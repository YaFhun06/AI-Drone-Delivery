import unittest
from app import create_app
from app.extensions import db
from app.models.drone import Drone

class DroneTestCase(unittest.TestCase):
    def setUp(self):
        """Khởi tạo môi trường test trước mỗi case"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Dọn dẹp DB sau mỗi case"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_drone(self):
        """Test API tạo mới Drone (CNPM-80)"""
        response = self.client.post('/api/drones', json={
            'name': 'Test Drone 01',
            'battery_level': 100,
            'status': 'IDLE'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Test Drone 01', response.get_data(as_text=True))

    def test_confirm_return(self):
        """Test API xác nhận Drone quay về (CNPM-81)"""
        with self.app.app_context():
            drone = Drone(name='Drone Return Test', status='DELIVERING', battery_level=90)
            db.session.add(drone)
            db.session.commit()
            drone_id = drone.id

        response = self.client.post(f'/api/drones/{drone_id}/confirm-return', json={
            'status': 'RETURNING',
            'battery_level': 75
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('RETURNING', response.get_data(as_text=True))

    def test_drone_model_instance(self):
        """Test khởi tạo dữ liệu trực tiếp từ Model Drone (CNPM-82)"""
        with self.app.app_context():
            drone = Drone(name='Drone Model Test', status='IDLE', battery_level=80)
            db.session.add(drone)
            db.session.commit()

            self.assertIsNotNone(drone.id)
            self.assertEqual(drone.battery_level, 80)

if __name__ == '__main__':
    unittest.main()