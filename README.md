# Transkribus Metagrapho API Client

![Tests](https://github.com/jnphilipp/transkribus_metagrapho_api/actions/workflows/tests.yml/badge.svg)

## Usage

### with ContextManager

```python
from time import sleep
from transkribus_metagrapho_api import transkribus_metagrapho_api

with transkribus_metagrapho_api(USERNAME, PASSWORD) as api:
    process_id = api.process(IMAGE_PATH, line_detection=49272, htr_id=51170)
    while True:
        match api.status(process_id).upper():
            case "FINISHED":
                print(api.apge(process_id))
                break
            case "FAILED":
                print("FAILED")
                break
        sleep(10)
```

or

```python
with transkribus_metagrapho_api(USERNAME, PASSWORD) as api:
    for image_path, page_xml in zip(IMAGES, api(IMAGES*, line_detection=49272, htr_id=51170)):
        with open(
            Path(image_path.parent, image_path.name.replace(image_path.suffix, ".xml")),
            "w",
            encoding="utf8"
        ) as f:
            f.write(page_xml)
```

### from command line

```bash
$ python3 -m transkribus_metagrapho_api --username USERNAME --password PASSWORD --images images/*.tiff
```
