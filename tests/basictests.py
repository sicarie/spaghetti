import unittest
from app import create_app, db
from app.models import User, Group

class BasicTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('instance/config.py')
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_register_user(self):
        response = self.client.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User registered successfully', response.data)

    def test_login_user(self):
        self.client.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)

    # Add more tests for other endpoints

if __name__ == '__main__':
    unittest.main()
