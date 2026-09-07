import React, { useState, useEffect } from 'react';
import { getDrones, createDrone, deleteDrone } from '../services/droneService';

const DroneList = () => {
  const [drones, setDrones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // State cho Form thêm Drone
  const [showAddForm, setShowAddForm] = useState(false);
  const [name, setName] = useState('');
  const [batteryLevel, setBatteryLevel] = useState(100);
  const [stationId, setStationId] = useState(1);
  const [submitting, setSubmitting] = useState(false);

  const fetchDrones = async () => {
    try {
      setLoading(true);
      const data = await getDrones();
      setDrones(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDrones();
  }, []);

  const handleCreateDrone = async (e) => {
    e.preventDefault();
    try {
      setSubmitting(true);
      await createDrone({
        name: name.trim(),
        battery_level: Number(batteryLevel),
        station_id: stationId ? Number(stationId) : null,
        status: 'IDLE',
      });
      setName('');
      setShowAddForm(false);
      fetchDrones();
    } catch (err) {
      alert(`Không thể thêm Drone: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteDrone = async (droneId) => {
    if (!window.confirm(`Xác nhận xóa Drone #${droneId}?`)) return;
    try {
      await deleteDrone(droneId);
      fetchDrones();
    } catch (err) {
      alert(`Lỗi khi xóa Drone: ${err.message}`);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mt-8">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Quản Lý Drone</h2>
          <span className="text-xs text-gray-500">Giám sát hoạt động, pin và trạm phụ trách</span>
        </div>
        <div className="flex items-center gap-3">
          <span className="bg-indigo-100 text-indigo-800 text-sm font-semibold px-3 py-1 rounded-full">
            Tổng số: {drones.length} drone
          </span>
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium px-4 py-1.5 rounded transition"
          >
            {showAddForm ? 'Đóng form' : '+ Thêm Drone'}
          </button>
        </div>
      </div>

      {/* Form tạo mới Drone */}
      {showAddForm && (
        <form onSubmit={handleCreateDrone} className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200 grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
          <div>
            <label className="block text-xs font-semibold text-gray-600 mb-1">Tên Drone *</label>
            <input
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="VD: Drone A1"
              className="w-full px-3 py-1.5 border rounded text-sm focus:outline-none focus:border-indigo-500"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-gray-600 mb-1">Mức pin (%)</label>
            <input
              type="number"
              min="0"
              max="100"
              value={batteryLevel}
              onChange={(e) => setBatteryLevel(e.target.value)}
              className="w-full px-3 py-1.5 border rounded text-sm focus:outline-none focus:border-indigo-500"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-gray-600 mb-1">ID Trạm quản lý</label>
            <input
              type="number"
              value={stationId}
              onChange={(e) => setStationId(e.target.value)}
              className="w-full px-3 py-1.5 border rounded text-sm focus:outline-none focus:border-indigo-500"
            />
          </div>
          <button
            type="submit"
            disabled={submitting}
            className="bg-green-600 hover:bg-green-700 text-white font-medium py-1.5 px-4 rounded text-sm transition disabled:opacity-50"
          >
            {submitting ? 'Đang lưu...' : 'Lưu Drone'}
          </button>
        </form>
      )}

      {loading && <p className="text-gray-500 animate-pulse mb-4">Đang tải danh sách drone...</p>}

      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-md border border-red-200 mb-4">
          <p className="font-semibold">Lỗi tải dữ liệu drone:</p>
          <p className="text-sm">Vui lòng kiểm tra backend ({error})</p>
        </div>
      )}

      {!loading && !error && (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-gray-600">
            <thead className="bg-gray-50 text-gray-700 uppercase text-xs font-semibold">
              <tr>
                <th className="px-4 py-3 border-b">ID</th>
                <th className="px-4 py-3 border-b">Tên Drone</th>
                <th className="px-4 py-3 border-b">Pin</th>
                <th className="px-4 py-3 border-b">Trạm Quản Lý</th>
                <th className="px-4 py-3 border-b">Trạng Thái</th>
                <th className="px-4 py-3 border-b text-right">Thao Tác</th>
              </tr>
            </thead>
            <tbody>
              {drones.length > 0 ? (
                drones.map((drone) => (
                  <tr key={drone.id} className="border-b hover:bg-gray-50">
                    <td className="px-4 py-3 font-medium text-indigo-600">#{drone.id}</td>
                    <td className="px-4 py-3 font-semibold text-gray-800">{drone.name}</td>
                    <td className="px-4 py-3">
                      <span className={`font-semibold ${drone.battery_level < 20 ? 'text-red-500' : 'text-green-600'}`}>
                        {drone.battery_level}%
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      {drone.station_id ? `Trạm #${drone.station_id}` : 'Chưa gán'}
                    </td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        drone.status === 'ACTIVE' ? 'bg-green-100 text-green-700' :
                        drone.status === 'RETURNING' ? 'bg-yellow-100 text-yellow-700' : 'bg-gray-100 text-gray-700'
                      }`}>
                        {drone.status || 'IDLE'}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-right">
                      <button
                        onClick={() => handleDeleteDrone(drone.id)}
                        className="text-red-500 hover:text-red-700 font-medium text-xs"
                      >
                        Xóa
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="6" className="px-4 py-8 text-center text-gray-500">
                    Chưa có drone nào trong hệ thống.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default DroneList;