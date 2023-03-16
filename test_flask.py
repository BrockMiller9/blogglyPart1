import unittest
from app import app, db
from models import User, Post


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class FlaskTests(unittest.TestCase):

    def setUp(self):
        """Add a test user to the database"""

        User.query.delete()

        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Users", html)

    def test_create_user(self):
        with app.test_client() as client:
            d = {"first_name": "John", "last_name": "Doe"}
            resp = client.post("/", data=d, follow_redirects=True)
            html = resp.get_data
