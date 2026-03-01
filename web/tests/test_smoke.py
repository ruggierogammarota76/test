import os

# Use in-memory SQLite for CI and tests
os.environ.setdefault('DATABASE_URL', 'sqlite:///:memory:')

from app import app
from models import db, User


def test_create_user_and_query():
    with app.app_context():
        db.create_all()
        u = User(username='ciuser', password_hash='x')
        db.session.add(u)
        db.session.commit()
        assert User.query.filter_by(username='ciuser').first() is not None
