# computer vision project

use `client.py` for testing the logic
use `rasptest.py` for raspberry pi testing

## install

```bash
python -m pip install -r requirements.txt
```

## run server

```bash
gunicorn -w 4 -b 0.0.0.0 'server:app'
```
