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
        setStations(stationRes || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="p-8 text-center bg-white rounded-2xl border border-slate-150 shadow-sm mt-6">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mb-2"></div>
        <p className="text-sm text-slate-500 font-medium">Đang đồng bộ dữ liệu vận hành từ Supabase...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-rose-50 text-rose-700 p-5 rounded-2xl border border-rose-200 mt-6 shadow-sm">
        <p className="font-semibold text-sm">Lỗi kết nối Dashboard Charts:</p>
        <p className="text-xs mt-1 text-rose-600">{error}</p>
      </div>
    );
  }

  // Phân bổ dữ liệu phòng vệ (Defensive Fallback) từ bảng trạng thái
  const byStatus = statusData?.by_status || {};
  const totalOrders = 
    successData?.total_orders || 
    statusData?.total_orders || 
    Object.values(byStatus).reduce((a, b) => a + b, 0);

  const completedOrders = 
    (successData?.completed && successData.completed > 0) 
      ? successData.completed 
      : (byStatus['DELIVERED'] || 0) + (byStatus['COMPLETED'] || 0);

  const inProgressOrders = 
    (successData?.in_progress && successData.in_progress > 0)
      ? successData.in_progress
      : (byStatus['APPROVED'] || 0) + (byStatus['IN_TRANSIT'] || 0) + (byStatus['ASSIGNED'] || 0);

  const failedOrders = 
    (successData?.failed && successData.failed > 0)
      ? successData.failed
      : (byStatus['FAILED'] || 0) + (byStatus['CANCELLED'] || 0);

  const maxStationOrders = Math.max(...stations.map((s) => s.orders_handled || 0), 1);

  // Bảng màu trực quan theo từng loại trạng thái (Task 5: Polish UI)
  const getStatusColor = (status) => {
    switch (status) {
      case 'DELIVERED':
      case 'COMPLETED':
        return { bar: 'bg-emerald-500', text: 'text-emerald-700', badge: 'bg-emerald-50' };
      case 'APPROVED':
      case 'PENDING':
        return { bar: 'bg-blue-500', text: 'text-blue-700', badge: 'bg-blue-50' };
      case 'IN_TRANSIT':
        return { bar: 'bg-amber-500', text: 'text-amber-700', badge: 'bg-amber-50' };
      case 'FAILED':
      case 'CANCELLED':
        return { bar: 'bg-rose-500', text: 'text-rose-700', badge: 'bg-rose-50' };
      default:
        return { bar: 'bg-indigo-500', text: 'text-indigo-700', badge: 'bg-indigo-50' };
    }
  };

  return (
    <div className="bg-white p-5 sm:p-6 rounded-2xl shadow-sm border border-slate-150 transition-all">
      {/* Tiêu đề & Trạng thái kết nối */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
        <div>
          <h2 className="text-lg sm:text-xl font-bold text-slate-800 tracking-tight">
            Bảng Chỉ Số & Biểu Đồ Vận Hành
          </h2>
          <span className="text-xs text-slate-500">Giám sát hiệu suất giao hàng và phân bố đơn</span>
        </div>
        <div className="flex items-center gap-2 self-start sm:self-auto">
          <span className="relative flex h-2.5 w-2.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
          </span>
          <span className="text-xs font-semibold px-2.5 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full">
            Hệ thống hoạt động
          </span>
        </div>
      </div>

      {/* KPI Cards: Tối ưu Responsive 1 cột trên mobile nhỏ, 2 cột tablet, 4 cột desktop */}
      <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 mb-6">
        <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl">
          <p className="text-xs text-slate-500 font-medium">Tổng số đơn</p>
          <p className="text-2xl font-bold text-slate-800 mt-1">{totalOrders}</p>
        </div>
        <div className="p-4 bg-blue-50 border border-blue-100 rounded-xl">
          <p className="text-xs text-blue-600 font-medium">Đang xử lý / Bay</p>
          <p className="text-2xl font-bold text-blue-700 mt-1">{inProgressOrders}</p>
        </div>
        <div className="p-4 bg-emerald-50 border border-emerald-100 rounded-xl">
          <p className="text-xs text-emerald-600 font-medium">Hoàn thành</p>
          <p className="text-2xl font-bold text-emerald-700 mt-1">{completedOrders}</p>
        </div>
        <div className="p-4 bg-rose-50 border border-rose-100 rounded-xl">
          <p className="text-xs text-rose-600 font-medium">Thất bại</p>
          <p className="text-2xl font-bold text-rose-700 mt-1">{failedOrders}</p>
        </div>
      </div>

      {/* Lưới hiển thị Biểu đồ */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Phân bố trạng thái đơn */}
        <div className="p-5 border border-slate-200 rounded-xl bg-slate-50/50">
          <h3 className="text-sm font-bold text-slate-700 mb-4">Phân Bố Trạng Thái Đơn Hàng</h3>
          {Object.keys(byStatus).length > 0 ? (
            <div className="space-y-4">
              {Object.entries(byStatus).map(([status, count]) => {
                const percent = totalOrders > 0 ? Math.round((count / totalOrders) * 100) : 0;
                const style = getStatusColor(status);
                return (
                  <div key={status} className="space-y-1.5">
                    <div className="flex justify-between text-xs font-semibold">
                      <span className={`px-2 py-0.5 rounded-md text-[11px] font-bold ${style.badge} ${style.text}`}>
                        {status}
                      </span>
                      <span className="text-slate-500">{count} đơn ({percent}%)</span>
                    </div>
                    <div className="w-full bg-slate-200 h-2.5 rounded-full overflow-hidden">
                      <div
                        className={`${style.bar} h-2.5 rounded-full transition-all duration-500`}
                        style={{ width: `${percent}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center py-8 text-xs text-slate-400">Chưa ghi nhận đơn hàng nào.</div>
          )}
        </div>

        {/* Phân bổ đơn theo trạm */}
        <div className="p-5 border border-slate-200 rounded-xl bg-slate-50/50">
          <h3 className="text-sm font-bold text-slate-700 mb-4">Tải Đơn Theo Từng Trạm</h3>
          {stations.length > 0 ? (
            <div className="space-y-4">
              {stations.map((st) => {
                const count = st.orders_handled || 0;
                const percent = Math.round((count / maxStationOrders) * 100);
                return (
                  <div key={st.station_id} className="space-y-1.5">
                    <div className="flex justify-between text-xs font-semibold">
                      <span className="text-slate-700">{st.station_name || `Trạm #${st.station_id}`}</span>
                      <span className="text-indigo-600 font-bold">{count} đơn</span>
                    </div>
                    <div className="w-full bg-slate-200 h-2.5 rounded-full overflow-hidden">
                      <div
                        className="bg-indigo-500 h-2.5 rounded-full transition-all duration-500"
                        style={{ width: `${percent}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center py-8 text-xs text-slate-400">Chưa ghi nhận dữ liệu theo trạm.</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DashboardCharts;