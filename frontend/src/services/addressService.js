const API_BASE_URL = 'http://127.0.0.1:5000';

const authHeaders = () => ({
  'Content-Type': 'application/json',
  Authorization: `Bearer ${localStorage.getItem('access_token')}`,
});

export const addressService = {
  async getAll() {
    const res = await fetch(`${API_BASE_URL}/api/addresses`, { headers: authHeaders() });
    return res.json();
  },
  async create(data) {
    const res = await fetch(`${API_BASE_URL}/api/addresses`, {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify(data),
    });
    return res.json();
  },
  async update(id, data) {
    const res = await fetch(`${API_BASE_URL}/api/addresses/${id}`, {
      method: 'PUT',
      headers: authHeaders(),
      body: JSON.stringify(data),
    });
    return res.json();
  },
  async remove(id) {
    const res = await fetch(`${API_BASE_URL}/api/addresses/${id}`, {
      method: 'DELETE',
      headers: authHeaders(),
    });
    return res.json();
  },
};