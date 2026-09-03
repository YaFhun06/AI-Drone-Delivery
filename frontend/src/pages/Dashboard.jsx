import React, { useState, useEffect } from 'react';
import { getOrdersByStatus } from '../services/analyticsService';

const Dashboard = () => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true);
        const data = await getOrdersByStatus();
        setAnalyticsData(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Tổng Quan Hệ Thống</h1>
      
      {/* Trạng thái đang tải */}
      {loading && <p className="text-gray-500 animate-pulse">Đang kết nối Backend để lấy dữ liệu...</p>}
      
      {/* Trạng thái lỗi (hiện ra khi backend chưa chạy) */}
      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-md border border-red-200">
          <p className="font-semibold">Chưa thể hiển thị thống kê:</p>
          <p className="text-sm">Vui lòng chờ Backend khởi động ({error})</p>
        </div>
      )}
      
      {/* Trạng thái gọi API thành công */}
      {!loading && !error && analyticsData && (
        <div>
          {/* Box Tổng số đơn hàng */}
          <div className="mb-8 p-5 bg-blue-50 border border-blue-200 rounded-lg inline-block min-w-[200px]">
            <p className="text-sm text-blue-600 font-semibold uppercase mb-1">Tổng Số Đơn Hàng</p>
            <p className="text-4xl font-bold text-blue-800">{analyticsData.total_orders}</p>
          </div>

          {/* Grid chi tiết theo trạng thái (Dùng Object.entries vì by_status là dictionary) */}
          <h2 className="text-lg font-semibold text-gray-700 mb-4">Chi tiết trạng thái đơn hàng</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(analyticsData.by_status).map(([status, count]) => (
              <div key={status} className="bg-gray-50 p-4 rounded-md border border-gray-200 text-center shadow-sm">
                <p className="text-sm text-gray-600 font-medium mb-1">{status}</p>
                <p className="text-2xl font-bold text-gray-800">{count}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;