import React, { useState, useEffect } from 'react';
import { getStations } from '../services/stationService';

const StationList = () => {
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStations = async () => {
      try {
        setLoading(true);
        const data = await getStations();
        setStations(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchStations();
  }, []);

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mt-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold text-gray-800">Quản Lý Trạm (Station)</h2>
        <span className="bg-purple-100 text-purple-800 text-sm font-semibold px-3 py-1 rounded-full">
          Tổng số: {stations.length} trạm
        </span>
      </div>

      {loading && <p className="text-gray-500 animate-pulse mb-4">Đang tải danh sách trạm...</p>}
      
      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-md border border-red-200 mb-4">
          <p className="font-semibold">Lỗi tải dữ liệu trạm:</p>
          <p className="text-sm">Vui lòng chờ Backend khởi động ({error})</p>
        </div>
      )}

      {!loading && !error && (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-gray-600">
            <thead className="bg-gray-50 text-gray-700 uppercase text-xs font-semibold">
              <tr>
                <th className="px-4 py-3 border-b">ID</th>
                <th className="px-4 py-3 border-b">Tên Trạm</th>
                <th className="px-4 py-3 border-b">Vị Trí</th>
                <th className="px-4 py-3 border-b">Sức Chứa</th>
                <th className="px-4 py-3 border-b">Trạng Thái</th>
              </tr>
            </thead>
            <tbody>
              {stations.length > 0 ? (
                stations.map((station, index) => (
                  <tr key={station.id || index} className="border-b hover:bg-gray-50">
                    <td className="px-4 py-3 font-medium text-purple-600">#{station.id}</td>
                    <td className="px-4 py-3">{station.name || 'N/A'}</td>
                    <td className="px-4 py-3">{station.location || 'N/A'}</td>
                    <td className="px-4 py-3">{station.capacity || 0} drone</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        station.status === 'Active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
                      }`}>
                        {station.status || 'Unknown'}
                      </span>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5" className="px-4 py-8 text-center text-gray-500">
                    Chưa có trạm nào trong hệ thống.
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

export default StationList;