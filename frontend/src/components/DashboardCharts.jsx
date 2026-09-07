import React, { useState, useEffect } from 'react';
import {
  getDeliverySuccessRate,
  getOrdersByStatus,
  getStationPerformance,
} from '../services/analyticsService';

const DashboardCharts = () => {
  const [successData, setSuccessData] = useState(null);
  const [statusData, setStatusData] = useState(null);
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [rateRes, statusRes, stationRes] = await Promise.all([
          getDeliverySuccessRate(),
          getOrdersByStatus(),
          getStationPerformance(),
        ]);
        setSuccessData(rateRes);
        setStatusData(statusRes);
        setStations(stationRes);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return <div className="p-6 text-gray-500 animate-pulse">Đang nạp dữ liệu Dashboard...</div>;
  }

  if (error) {
    return (
      <div className="bg-red-50 text-red-600 p-4 rounded-lg border border-red-200 mt-6">
        <p className="font-semibold">Lỗi tải Dashboard Charts:</p>
        <p className="text-sm">{error}</p>
      </div>
    );
  }

  const maxStationOrders = Math.max(...stations.map((s) => s.orders_handled || 0), 1);

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mt-8">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Bảng Chỉ Số & Biểu Đồ Vận Hành</h2>
          <span className="text-xs text-gray-500">Giám sát hiệu suất giao hàng và phân bố đơn</span>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 bg-green-100 text-green-800 rounded-full">
          Hệ thống hoạt động
        </span>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="p-4 bg-slate-50 border rounded-lg">
          <p className="text-xs text-gray-500 font-medium">Tổng số đơn</p>
          <p className="text-2xl font-bold text-slate-800">{successData?.total_orders || 0}</p>
        </div>
        <div className="p-4 bg-blue-50 border border-blue-100 rounded-lg">
          <p className="text-xs text-blue-600 font-medium">Đang xử lý / Bay</p>
          <p className="text-2xl font-bold text-blue-800">{successData?.in_progress || 0}</p>
        </div>
        <div className="p-4 bg-green-50 border border-green-100 rounded-lg">
          <p className="text-xs text-green-600 font-medium">Hoàn thành</p>
          <p className="text-2xl font-bold text-green-800">{successData?.completed || 0}</p>
        </div>
        <div className="p-4 bg-red-50 border border-red-100 rounded-lg">
          <p className="text-xs text-red-600 font-medium">Thất bại</p>
          <p className="text-2xl font-bold text-red-800">{successData?.failed || 0}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Biểu đồ phân bố trạng thái đơn */}
        <div className="p-4 border rounded-lg bg-gray-50">
          <h3 className="text-sm font-bold text-gray-700 mb-4">Phân Bố Trạng Thái Đơn Hàng</h3>
          {statusData?.by_status && Object.keys(statusData.by_status).length > 0 ? (
            <div className="space-y-3">
              {Object.entries(statusData.by_status).map(([status, count]) => {
                const total = statusData.total_orders || 1;
                const percent = Math.round((count / total) * 100);
                return (
                  <div key={status}>
                    <div className="flex justify-between text-xs font-semibold mb-1">
                      <span className="text-gray-700">{status}</span>
                      <span className="text-gray-500">{count} đơn ({percent}%)</span>
                    </div>
                    <div className="w-full bg-gray-200 h-2.5 rounded-full overflow-hidden">
                      <div
                        className="bg-indigo-600 h-2.5 rounded-full"
                        style={{ width: `${percent}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <p className="text-xs text-gray-400">Chưa có đơn hàng nào.</p>
          )}
        </div>

        {/* Biểu đồ tải đơn theo trạm */}
        <div className="p-4 border rounded-lg bg-gray-50">
          <h3 className="text-sm font-bold text-gray-700 mb-4">Tải Đơn Theo Từng Trạm</h3>
          {stations.length > 0 ? (
            <div className="space-y-3">
              {stations.map((st) => {
                const percent = Math.round(((st.orders_handled || 0) / maxStationOrders) * 100);
                return (
                  <div key={st.station_id}>
                    <div className="flex justify-between text-xs font-semibold mb-1">
                      <span className="text-gray-700">{st.station_name || `Trạm #${st.station_id}`}</span>
                      <span className="text-indigo-600">{st.orders_handled || 0} đơn</span>
                    </div>
                    <div className="w-full bg-gray-200 h-2.5 rounded-full overflow-hidden">
                      <div
                        className="bg-teal-500 h-2.5 rounded-full"
                        style={{ width: `${percent}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <p className="text-xs text-gray-400">Chưa ghi nhận dữ liệu theo trạm.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default DashboardCharts;