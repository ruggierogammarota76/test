from app import app
from models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='testuser').first():
        u = User(username='testuser', password_hash=generate_password_hash('testpass'))
        db.session.add(u)
        db.session.commit()
        print('Created test user: testuser / testpass')
    else:
        print('Test user already exists')
