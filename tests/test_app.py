import unittest
import os
from app import app, db
from config import config_by_name

class DMScriptorTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_login_page_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'DM Scriptor', response.data)
    
    def test_login_with_wrong_password(self):
        response = self.app.post('/', data={'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid password', response.data)
    
    def test_login_with_correct_password(self):
        with app.app_context():
            os.environ['PASSWORD'] = 'testpass'
            response = self.app.post('/', data={'password': 'testpass'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'DM Scriptor', response.data)
    
    def test_scriptor_requires_login(self):
        response = self.app.get('/scriptor')
        self.assertEqual(response.status_code, 302)
    
    def test_logout(self):
        with self.app.session_transaction() as sess:
            sess['logged_in'] = True
        
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'DM Scriptor', response.data)
    
    def test_api_scripts_requires_login(self):
        response = self.app.get('/api/scripts')
        self.assertEqual(response.status_code, 401)
    
    def test_404_error_page(self):
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404', response.data)

if __name__ == '__main__':
    unittest.main()