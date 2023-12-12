# Transkribus Metagrapho API Client

![Tests](https://github.com/jnphilipp/transkribus_metagrapho_api/actions/workflows/tests.yml/badge.svg)

## Usage

### with ContextManager

```python
from time import sleep
from transkribus_metagrapho_api import transkribus_metagrapho_api

with transkribus_metagrapho_api(USERNAME, PASSWORD) as api:
    process_id = api.process(IMAGE_PATH, line_detection=49272, htr_id=51170)
    while not api.is_finished(process_id):
        sleep(10)
    print(api.page(process_id))
```

### from command line

```bash
$ python3 -m transkribus_metagrapho_api --username USERNAME --password PASSWORD --images images/*.tiff
```
