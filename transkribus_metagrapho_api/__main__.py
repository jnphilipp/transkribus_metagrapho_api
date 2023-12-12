#!/usr/bin/env python3
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
"""Transkribus Metagrapho API Client."""

import sys

import transkribus_metagrapho_api.app

if __name__ == "__main__":
    sys.exit(transkribus_metagrapho_api.app.main())
