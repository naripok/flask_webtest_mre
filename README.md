# Minimal reproducible example for Flask-Webtest session management bug

This is a MRE for the Flask-Webtest session management bug mentioned in the [issue](https://github.com/level12/flask-webtest/issues/25).

## Running

Install, run, check that `test_original_get_scopefunc` fails:

```
pipenv install --dev
pytest
```
