import React, { useEffect, useState } from 'react';
import { fetchStations } from '../services/stationService';

export default function StationList() {
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStations().then(data => {
      setStations(data);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return <div className="p-6 text-center text-gray-500">Đang tải danh sách trạm đáp...</div>;
  }

  return (
    <div className="p-6 bg-white rounded-xl shadow-md">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Quản Lý Trạm Đáp</h2>
        <span className="bg-purple-100 text-purple-700 text-sm font-semibold px-3 py-1 rounded-full">
          Tổng số: {stations.length} trạm
        </span>
      </div>

      <div className="overflow-x-auto border border-gray-100 rounded-lg">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Mã Trạm</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tên Trạm</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Trạng Thái</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Pin</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Drone Hoạt Động</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {stations.map((station) => (
              <tr key={station.id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{station.id}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{station.name}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                   <span className={`px-2.5 py-1 text-xs font-semibold rounded-full ${
                    station.status === 'Hoạt động' ? 'bg-green-100 text-green-700' : 'bg-orange-100 text-orange-700'
                  }`}>
                    {station.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{station.battery}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{station.dronesActive}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}