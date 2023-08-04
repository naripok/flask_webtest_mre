import pytest
from flask import Flask
from flask.globals import app_ctx
from flask_sqlalchemy import SQLAlchemy
from flask_webtest import get_scopefunc

session_options = {
    "scopefunc": get_scopefunc(
        # mimics the original sqlalchemy implementaion
        # def _app_ctx_id() -> int:
        #     """Get the id of the current Flask application context for the session scope."""
        #     return id(app_ctx._get_current_object())  # type: ignore[attr-defined]
        original_scopefunc=lambda: id(app_ctx._get_current_object())
    )
}
db = SQLAlchemy(session_options=session_options)


class Event(db.Model):
    id = db.Column(db.Integer(), primary_key=True)


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    db.init_app(app)
    return app


@pytest.fixture
def app():
    _app = create_app()
    with _app.test_request_context():
        yield _app


@pytest.fixture(name="db")
def fixture_db():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


def test_session_context(app, db):
    event = Event()
    db.session.add(event)
    db.session.commit()

    assert event in db.session

    with app.app_context():
        assert event not in db.session
