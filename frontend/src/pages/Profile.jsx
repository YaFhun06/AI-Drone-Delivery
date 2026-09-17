import React, { useEffect, useState } from 'react';

const API_BASE_URL = 'http://127.0.0.1:5000';

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [fullName, setFullName] = useState('');
  const [phone, setPhone] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem('access_token');

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/users/profile`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => {
        setProfile(data);
        setFullName(data.full_name || '');
        setPhone(data.phone || '');
        setLoading(false);
      });
  }, [token]);

  const handleSave = async (e) => {
    e.preventDefault();
    const res = await fetch(`${API_BASE_URL}/api/users/profile`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ full_name: fullName, phone }),
    });
    const data = await res.json();
    if (res.ok) {
      setMessage('Cập nhật hồ sơ thành công!');
    } else {
      setMessage(data.error || 'Cập nhật thất bại');
    }
  };

  if (loading) return <div className="p-6 text-center text-gray-500">Đang tải...</div>;

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 max-w-lg mx-auto">
      <h1 className="text-2xl font-bold text-gray-800 mb-4">Hồ sơ cá nhân</h1>
      {message && <p className="text-green-600 mb-4">{message}</p>}

      <form onSubmit={handleSave}>
        <div className="mb-4">
          <label className="block text-sm text-gray-500 mb-1">Email</label>
          <input type="text" value={profile?.email || ''} disabled className="w-full p-2 border rounded bg-gray-100" />
        </div>
        <div className="mb-4">
          <label className="block text-sm text-gray-500 mb-1">Họ tên</label>
          <input
            type="text"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            className="w-full p-2 border rounded"
          />
        </div>
        <div className="mb-4">
          <label className="block text-sm text-gray-500 mb-1">Số điện thoại</label>
          <input
            type="text"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            className="w-full p-2 border rounded"
          />
        </div>
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
          Lưu thay đổi
        </button>
      </form>
    </div>
  );
};

export default Profile;