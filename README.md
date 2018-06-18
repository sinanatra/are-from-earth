This is an example Flask application to highlight gender biases in a text.

Requisites
----------

Install PIP requirements with `pip install -r requirements.txt`.

Run:

```bash
mkdir -p templates/
mkdir -p static/
mv templates__index.html templates/index.html
mv static__index.js static/index.js
mv static__index.css static/index.css
```

Start
-----

Run `FLASK_APP=server.py flask run` to start.

Run `FLASK_APP=server.py FLASK_DEBUG=1 flask run` to start in debugging mode.
