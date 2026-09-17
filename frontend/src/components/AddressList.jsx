import React, { useEffect, useState } from 'react';
import { addressService } from '../services/addressService';

export default function AddressList() {
  const [addresses, setAddresses] = useState([]);
  const [form, setForm] = useState({ street: '', city: '', latitude: '', longitude: '' });
  const [loading, setLoading] = useState(true);

  const load = () => {
    addressService.getAll().then((data) => {
      setAddresses(Array.isArray(data) ? data : []);
      setLoading(false);
    });
  };

  useEffect(() => { load(); }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    await addressService.create({
      street: form.street,
      city: form.city,
      latitude: parseFloat(form.latitude),
      longitude: parseFloat(form.longitude),
    });
    setForm({ street: '', city: '', latitude: '', longitude: '' });
    load();
  };

  const handleDelete = async (id) => {
    await addressService.remove(id);
    load();
  };

  if (loading) return <div className="p-6 text-center text-gray-500">Đang tải...</div>;

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h1 className="text-2xl font-bold text-gray-800 mb-4">Địa chỉ giao hàng</h1>

      <form onSubmit={handleCreate} className="grid grid-cols-2 gap-3 mb-6">
        <input placeholder="Số nhà, đường" value={form.street}
          onChange={(e) => setForm({ ...form, street: e.target.value })}
          className="p-2 border rounded col-span-2" required />
        <input placeholder="Thành phố" value={form.city}
          onChange={(e) => setForm({ ...form, city: e.target.value })}
          className="p-2 border rounded col-span-2" />
        <input placeholder="Vĩ độ (latitude)" value={form.latitude}
          onChange={(e) => setForm({ ...form, latitude: e.target.value })}
          className="p-2 border rounded" required />
        <input placeholder="Kinh độ (longitude)" value={form.longitude}
          onChange={(e) => setForm({ ...form, longitude: e.target.value })}
          className="p-2 border rounded" required />
        <button type="submit" className="col-span-2 bg-blue-600 text-white p-2 rounded">
          Thêm địa chỉ
        </button>
      </form>

      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Địa chỉ</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Thành phố</th>
              <th className="px-4 py-2"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {addresses.map((a) => (
              <tr key={a.id}>
                <td className="px-4 py-2 text-sm">{a.street}</td>
                <td className="px-4 py-2 text-sm">{a.city}</td>
                <td className="px-4 py-2 text-right">
                  <button onClick={() => handleDelete(a.id)} className="text-red-600 text-sm">Xóa</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}