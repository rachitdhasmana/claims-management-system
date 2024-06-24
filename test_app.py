import os
import unittest
import tempfile
from app import app, db, Claim


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.temp_db = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{self.temp_db}'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.temp_db)

    def test_add_claim(self):
        with open('test_file.txt', 'w') as f:
            f.write('Test file content')
        with open('test_file.txt', 'rb') as f:
            response = self.app.post('/api/claims', data={
                'title': 'Test Claim',
                'description': 'Test Description',
                'claim_type': 'type 1',
                'claim_value': '100.0',
                'attachment': f
            })
        os.remove('test_file.txt')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], 'Test Claim')
        self.assertEqual(data['description'], 'Test Description')
        self.assertEqual(data['claim_type'], 'type 1')
        self.assertEqual(data['claim_value'], 100.0)
        self.assertEqual(data['status'], 'new')
        self.assertTrue(data['attachment'] is not None)

    def test_get_claims(self):
        self.test_add_claim()
        response = self.app.get('/api/claims')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Test Claim')

    def test_update_claim(self):
        self.test_add_claim()
        response = self.app.get('/api/claims')
        claim_id = response.get_json()[0]['id']
        response = self.app.put(f'/api/claims/{claim_id}', json={
            'title': 'Updated Title',
            'description': 'Updated Description',
            'claim_type': 'type 2',
            'claim_value': 200.0,
            'status': 'acknowledged'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], 'Updated Title')
        self.assertEqual(data['description'], 'Updated Description')
        self.assertEqual(data['claim_type'], 'type 2')
        self.assertEqual(data['claim_value'], 200.0)
        self.assertEqual(data['status'], 'acknowledged')

    def test_delete_claim(self):
        self.test_add_claim()
        response = self.app.get('/api/claims')
        pre_delete_count = len(response.get_json())
        claim_id = response.get_json()[0]['id']
        response = self.app.delete(f'/api/claims/{claim_id}')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/api/claims')
        post_delete_count = len(response.get_json())
        self.assertEqual(pre_delete_count - 1, post_delete_count)


if __name__ == '__main__':
    unittest.main()
