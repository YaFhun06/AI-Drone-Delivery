import pytest


class TestDroneEndpoints:
    def test_create_drone(self, client, auth_headers):
        response = client.post(
            '/api/drones',
            json={'name': 'Test Drone 01', 'battery_level': 100, 'status': 'IDLE'},
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == 'Test Drone 01'
        assert data['battery_level'] == 100

    def test_confirm_return(self, client, auth_headers):
        create_response = client.post(
            '/api/drones',
            json={'name': 'Drone Return Test', 'status': 'DELIVERING', 'battery_level': 90},
            headers=auth_headers,
        )
        drone_id = create_response.get_json()['id']

        response = client.post(
            f'/api/drones/{drone_id}/confirm-return',
            json={'status': 'RETURNING', 'battery_level': 75},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['drone']['status'] == 'RETURNING'
        assert data['drone']['battery_level'] == 75

    def test_get_drone(self, client, auth_headers):
        create_response = client.post(
            '/api/drones',
            json={'name': 'Drone Model Test', 'status': 'IDLE', 'battery_level': 80},
            headers=auth_headers,
        )
        drone_id = create_response.get_json()['id']

        response = client.get(f'/api/drones/{drone_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['battery_level'] == 80

    def test_get_drone_not_found(self, client):
        response = client.get('/api/drones/999')
        assert response.status_code == 404

    def test_delete_drone(self, client, auth_headers):
        create_response = client.post(
            '/api/drones',
            json={'name': 'Drone To Delete', 'battery_level': 50},
            headers=auth_headers,
        )
        drone_id = create_response.get_json()['id']

        response = client.delete(f'/api/drones/{drone_id}', headers=auth_headers)
        assert response.status_code == 200

        get_response = client.get(f'/api/drones/{drone_id}')
        assert get_response.status_code == 404