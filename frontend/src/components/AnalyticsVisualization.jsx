import React, { useState, useEffect } from 'react';
import {
  getOperatingCost,
  getDeliverySuccessRate,
  getOrdersByStatus,
} from '../services/analyticsService';

const AnalyticsVisualization = () => {
  const [costData, setCostData] = useState(null);
  const [rateData, setRateData] = useState(null);
  const [statusData, setStatusData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [costRes, rateRes, statusRes] = await Promise.all([
          getOperatingCost().catch(() => null),
          getDeliverySuccessRate().catch(() => null),
          getOrdersByStatus().catch(() => null),
        ]);
        setCostData(costRes);
        setRateData(rateRes);
        setStatusData(statusRes);
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
        <p className="text-sm text-slate-500 font-medium">Đang phân tích chi phí & hiệu suất...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-rose-50 text-rose-700 p-5 rounded-2xl border border-rose-200 mt-6 shadow-sm">
        <p className="font-semibold text-sm">Lỗi tải dữ liệu Analytics:</p>
        <p className="text-xs mt-1 text-rose-600">{error}</p>
      </div>
    );
  }

  // Cơ chế tính toán tỷ lệ thành công phòng vệ (Khắc phục lỗi 0% Đạt)
  const byStatus = statusData?.by_status || {};
  const totalOrders =
    statusData?.total_orders ||
    rateData?.total_orders ||
    Object.values(byStatus).reduce((a, b) => a + b, 0);

  const deliveredCount = (byStatus['DELIVERED'] || 0) + (byStatus['COMPLETED'] || 0);
  const failedCount = (byStatus['FAILED'] || 0) + (byStatus['CANCELLED'] || 0);

  // Ưu tiên tỷ lệ từ backend, nếu backend trả về 0 mà có đơn DELIVERED thì tự tính
  const calculatedSuccessRate =
    totalOrders > 0 ? Math.round((deliveredCount / totalOrders) * 100) : 0;
  const successPercent =
    rateData?.success_rate_percent && rateData.success_rate_percent > 0
      ? rateData.success_rate_percent
      : calculatedSuccessRate;

  const failurePercent =
    rateData?.failure_rate_percent && rateData.failure_rate_percent > 0
      ? rateData.failure_rate_percent
      : totalOrders > 0
      ? Math.round((failedCount / totalOrders) * 100)
      : 0;

  // Xử lý linh hoạt cả 2 kiểu đặt tên biến chi phí từ Backend
  const totalCost =
    costData?.estimated_total_cost_vnd ?? costData?.total_cost ?? 0;
  const avgCost =
    costData?.average_cost_per_order_vnd ?? costData?.average_cost_per_order ?? 0;
  const totalWeight =
    costData?.total_package_weight_kg ?? costData?.total_weight_kg ?? 0;

  const formatVND = (num) => (num ? Number(num).toLocaleString('vi-VN') + ' đ' : '0 đ');

  return (
    <div className="bg-white p-5 sm:p-6 rounded-2xl shadow-sm border border-slate-150 transition-all mt-6">
      {/* Tiêu đề */}
      <div className="mb-6">
        <h2 className="text-lg sm:text-xl font-bold text-slate-800 tracking-tight">
          Phân Tích Chi Phí & Hiệu Quả Giao Hàng
        </h2>
        <span className="text-xs text-slate-500">
          Ước tính tiêu hao năng lượng, tải trọng và tỷ lệ thành công nhiệm vụ (FR-29)
        </span>
      </div>

      {/* 3 Thẻ Chỉ số: Responsive 1 cột trên mobile nhỏ, 3 cột trên tablet/desktop */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        {/* Tổng chi phí */}
        <div className="p-4 sm:p-5 bg-indigo-50/60 border border-indigo-100 rounded-xl">
          <p className="text-xs font-semibold text-indigo-700 uppercase tracking-wider">
            Tổng Chi Phí Ước Tính
          </p>
          <p className="text-2xl font-black text-indigo-900 mt-2">
            {formatVND(totalCost)}
          </p>
          <p className="text-[11px] text-indigo-400 mt-1">Đơn vị: VNĐ</p>
        </div>

        {/* Chi phí TB / đơn */}
        <div className="p-4 sm:p-5 bg-amber-50/60 border border-amber-100 rounded-xl">
          <p className="text-xs font-semibold text-amber-700 uppercase tracking-wider">
            Chi Phí TB / Đơn Hàng
          </p>
          <p className="text-2xl font-black text-amber-900 mt-2">
            {formatVND(avgCost)}
          </p>
          <p className="text-[11px] text-amber-500 mt-1">Chi phí cơ bản + phụ phí tải</p>
        </div>

        {/* Tổng khối lượng */}
        <div className="p-4 sm:p-5 bg-emerald-50/60 border border-emerald-100 rounded-xl">
          <p className="text-xs font-semibold text-emerald-700 uppercase tracking-wider">
            Tổng Khối Lượng Hàng
          </p>
          <p className="text-2xl font-black text-emerald-900 mt-2">
            {totalWeight} kg
          </p>
          <p className="text-[11px] text-emerald-500 mt-1">Khối lượng kiện hàng đã nhận</p>
        </div>
      </div>

      {/* Biểu đồ tiến độ tỷ lệ hoàn thành */}
      <div className="p-5 border border-slate-200 rounded-xl bg-slate-50/50">
        <div className="flex justify-between items-center mb-3">
          <h3 className="text-sm font-bold text-slate-700">Hiệu Quả Hoàn Thành Giao Hàng</h3>
          <span className="text-sm font-bold text-emerald-600 px-2 py-0.5 bg-emerald-50 border border-emerald-200 rounded-lg">
            {successPercent}% Đạt
          </span>
        </div>

        {/* Thanh tiến độ đa màu (Thành công & Thất bại) */}
        <div className="w-full bg-slate-200 h-3.5 rounded-full overflow-hidden flex mb-3 shadow-inner">
          <div
            className="bg-emerald-500 h-3.5 transition-all duration-700"
            style={{ width: `${successPercent}%` }}
            title={`Giao thành công: ${successPercent}%`}
          ></div>
          <div
            className="bg-rose-500 h-3.5 transition-all duration-700"
            style={{ width: `${failurePercent}%` }}
            title={`Thất bại: ${failurePercent}%`}
          ></div>
        </div>

        {/* Chú thích trạng thái */}
        <div className="flex flex-wrap gap-4 text-xs">
          <span className="flex items-center gap-1.5 text-slate-700 font-medium">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span>
            Tỷ lệ giao thành công: {successPercent}%
          </span>
          <span className="flex items-center gap-1.5 text-slate-700 font-medium">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block"></span>
            Tỷ lệ sự cố / Thất bại: {failurePercent}%
          </span>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsVisualization;