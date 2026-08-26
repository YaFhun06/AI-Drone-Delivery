import pytest


class TestStationEndpoints:
    def test_create_station(self, client, auth_headers):
        response = client.post(
            '/api/stations',
            json={
                'name': 'Trạm A',
                'latitude': 21.0285,
                'longitude': 105.8542,
                'capacity': 10,
                'status': 'ACTIVE',
            },
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == 'Trạm A'
        assert data['capacity'] == 10
        assert data['status'] == 'ACTIVE'

    def test_list_stations(self, client, auth_headers):
        client.post(
            '/api/stations',
            json={
                'name': 'Trạm A',
                'latitude': 21.0285,
                'longitude': 105.8542,
                'capacity': 10,
                'status': 'ACTIVE',
            },
            headers=auth_headers,
        )
        response = client.get('/api/stations')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['name'] == 'Trạm A'

    def test_get_station(self, client, auth_headers):
        create_response = client.post(
            '/api/stations',
            json={
                'name': 'Trạm B',
                'latitude': 10.8231,
                'longitude': 106.6297,
                'capacity': 5,
                'status': 'ACTIVE',
            },
            headers=auth_headers,
        )
        station_id = create_response.get_json()['id']
        response = client.get(f'/api/stations/{station_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == 'Trạm B'

    def test_get_station_not_found(self, client):
        response = client.get('/api/stations/999')
        assert response.status_code == 404

    def test_update_station(self, client, auth_headers):
        create_response = client.post(
            '/api/stations',
            json={
                'name': 'Trạm C',
                'latitude': 16.0544,
                'longitude': 108.2022,
                'capacity': 8,
                'status': 'ACTIVE',
            },
            headers=auth_headers,
        )
        station_id = create_response.get_json()['id']
        response = client.put(
            f'/api/stations/{station_id}',
            json={'capacity': 12, 'latitude': 16.0544, 'longitude': 108.2022},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['capacity'] == 12

    def test_update_station_status(self, client, auth_headers):
        create_response = client.post(
            '/api/stations',
            json={
                'name': 'Trạm D',
                'latitude': 12.2388,
                'longitude': 109.1967,
                'capacity': 6,
                'status': 'ACTIVE',
            },
            headers=auth_headers,
        )
        station_id = create_response.get_json()['id']
        response = client.put(
            f'/api/stations/{station_id}/status',
            json={'status': 'MAINTENANCE', 'latitude': 12.2388, 'longitude': 109.1967},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'MAINTENANCE'

    def test_update_station_status_invalid(self, client, auth_headers):
        create_response = client.post(
            '/api/stations',
            json={
                'name': 'Trạm E',
                'latitude': 16.4637,
                'longitude': 107.5909,
                'capacity': 4,
                'status': 'ACTIVE',
            },
            headers=auth_headers,
        )
        station_id = create_response.get_json()['id']
        response = client.put(
            f'/api/stations/{station_id}/status',
            json={'status': 'INVALID'},
            headers=auth_headers,
        )
        assert response.status_code == 400

    def test_delete_station(self, client, auth_headers):
        create_response = client.post(
            '/api/stations',
            json={
                'name': 'Trạm F',
                'latitude': 20.8449,
                'longitude': 106.6881,
                'capacity': 3,
                'status': 'ACTIVE',
            },
            headers=auth_headers,
        )
        station_id = create_response.get_json()['id']
        response = client.delete(
            f'/api/stations/{station_id}',
            headers=auth_headers,
        )
        assert response.status_code == 200
        get_response = client.get(f'/api/stations/{station_id}')
        assert get_response.status_code == 404

    def test_get_capacity(self, client, auth_headers):
        create_response = client.post(
            '/api/stations',
            json={
                'name': 'Trạm G',
                'latitude': 21.0060,
                'longitude': 107.2920,
                'capacity': 15,
                'status': 'ACTIVE',
            },
            headers=auth_headers,
        )
        station_id = create_response.get_json()['id']
        response = client.get(f'/api/stations/{station_id}/capacity')
        assert response.status_code == 200
        data = response.get_json()
        assert data['capacity'] == 15
        assert data['active_orders'] == 0
        assert data['available'] == 15
