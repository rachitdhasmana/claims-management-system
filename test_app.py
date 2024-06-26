import unittest
from app import app, db, User, Claim
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt


class ClaimsManagementTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            self.create_test_data()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def create_test_data(self):
        password = 'password'
        bcrypt = Bcrypt(app)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        admin_user = User(username='admin', password=hashed_password, role='admin')
        normal_user = User(username='user', password=hashed_password, role='user')
        db.session.add(admin_user)
        db.session.add(normal_user)
        db.session.commit()

    def get_token(self, username):
        user = User.query.filter_by(username=username).first()
        return create_access_token(identity={'username': user.username, 'role': user.role})

    def test_register_user(self):
        response = self.app.post('/register', json={
            'username': 'newuser',
            'password': 'newpassword',
            'role': 'user'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', response.get_json()['message'])

    def test_login_user(self):
        response = self.app.post('/login', json={
            'username': 'user',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.get_json())

    def test_create_claim(self):
        with app.app_context():
            token = self.get_token('user')
            response = self.app.post('/api/claims', headers={
                'Authorization': f'Bearer {token}'
            }, data={
                'title': 'title 1',
                'description': 'desc 1',
                'type': 'type 1',
                'value': 100.0,
                'attachment': ''
            })
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.get_json()['type'], 'type 1')

    def test_get_claims_admin(self):
        with app.app_context():
            token = self.get_token('admin')
            response = self.app.get('/api/claims', headers={
                'Authorization': f'Bearer {token}'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.get_json(), list)

    def test_get_claims_user(self):
        with app.app_context():
            token = self.get_token('user')
            response = self.app.get('/api/claims', headers={
                'Authorization': f'Bearer {token}'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.get_json(), list)

    def test_update_claim(self):
        self.test_create_claim()
        with app.app_context():
            token = self.get_token('user')
            claim = Claim.query.first()
            response = self.app.put(f'/api/claims/{claim.id}', headers={
                'Authorization': f'Bearer {token}'
            }, json={
                'type': 'type 2',
                'value': 200.0
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()['type'], 'type 2')

    def test_delete_claim(self):
        self.test_create_claim()
        with app.app_context():
            token = self.get_token('admin')
            claim = Claim.query.first()
            response = self.app.delete(f'/api/claims/{claim.id}', headers={
                'Authorization': f'Bearer {token}'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn('Claim deleted', response.get_json()['message'])


if __name__ == '__main__':
    unittest.main()
