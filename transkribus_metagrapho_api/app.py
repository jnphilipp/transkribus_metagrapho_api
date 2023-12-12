# Copyright (C) 2023 J. Nathanael Philipp (jnphilipp) <nathanael@philipp.land>
#
# Transkribus Metagrapho API Client
#
# This file is part of transkribus-metagrapho-api.
#
# transkribus-metagrapho-api is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# transkribus-metagrapho-api is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar. If not, see <http://www.gnu.org/licenses/>
"""Transkribus Metagrapho API Client cmd interface."""

import logging
import sys

from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    RawTextHelpFormatter,
)
from pathlib import Path
from typing import List

from . import VERSION
from .api import transkribus_metagrapho_api


class ArgFormatter(ArgumentDefaultsHelpFormatter, RawTextHelpFormatter):
    """Combination of ArgumentDefaultsHelpFormatter and RawTextHelpFormatter."""

    pass


def filter_info(rec: logging.LogRecord) -> bool:
    """Log record filter for info and lower levels.

    Args:
     * rec: LogRecord object
    """
    return rec.levelno <= logging.INFO


def main():
    """Run the command line interface."""
    parser = ArgumentParser(
        prog="transkribus_metagrapho_api", formatter_class=ArgFormatter
    )
    parser.add_argument("-V", "--version", action="version", version=VERSION)

    parser.add_argument("-u", "--username", required=True, help="username.")
    parser.add_argument("-p", "--password", required=True, help="password.")

    parser.add_argument(
        "-i",
        "--images",
        nargs="*",
        type=lambda p: Path(p).absolute(),
        help="images to process.",
    )

    parser.add_argument(
        "--line-detection-model",
        type=int,
        default=49272,
        help="line detection model ID.",
    )
    parser.add_argument(
        "--text-recognition-model",
        type=int,
        default=51170,
        help="text recognition model ID.",
    )
    parser.add_argument(
        "--language-model",
        type=int,
        help="language model ID.",
    )
    parser.add_argument(
        "--sleep",
        type=int,
        default=5,
        help="wait time between check status requests, in seconds.",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--page",
        default=True,
        action="store_true",
        help="Store results as PAGE-XML files.",
    )
    group.add_argument(
        "--alto", action="store_true", help="Store results as ALTO-XML files."
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="verbosity level; multiple times increases the level, the maximum is 3, "
        + "for debugging.",
    )
    parser.add_argument(
        "--log-format",
        default="%(message)s",
        help="set logging format.",
    )
    parser.add_argument(
        "--log-file",
        type=lambda p: Path(p).absolute(),
        help="log output to a file.",
    )

    args = parser.parse_args()

    if args.verbose == 0:
        level = logging.WARNING
    elif args.verbose == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG

    handlers: List[logging.Handler] = []
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(level)
    stdout_handler.addFilter(filter_info)
    handlers.append(stdout_handler)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    if "%(levelname)s" not in args.log_format:
        stderr_handler.setFormatter(
            logging.Formatter(f"[%(levelname)s] {args.log_format}")
        )
    handlers.append(stderr_handler)

    if args.log_file:
        file_handler = logging.FileHandler(args.log_file)
        file_handler.setLevel(level)
        if args.log_file_format:
            file_handler.setFormatter(logging.Formatter(args.log_file_format))
        handlers.append(file_handler)

    logging.basicConfig(
        format=args.log_format,
        level=logging.DEBUG,
        handlers=handlers,
    )

    mode = None
    if args.alto:
        mode = "alto"
    elif args.page:
        mode = "page"
    xmls = []
    with transkribus_metagrapho_api(args.username, args.password) as api:
        if len(args.images) > 0:
            xmls = api(
                *args.images,
                line_detection=args.line_detection_model,
                htr_id=args.text_recognition_model,
                language_model=args.language_model,
                mode=mode,
                wait=args.sleep,
            )

    for path, xml in zip(args.images, xmls):
        with open(path.with_suffix(".xml"), "w", encoding="utf8") as f:
            f.write(xml)
            f.write("\n")
