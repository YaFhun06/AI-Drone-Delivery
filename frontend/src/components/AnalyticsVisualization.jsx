import React, { useState, useEffect } from 'react';
import { getOperatingCost, getDeliverySuccessRate } from '../services/analyticsService';

const AnalyticsVisualization = () => {
  const [costData, setCostData] = useState(null);
  const [rateData, setRateData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [costRes, rateRes] = await Promise.all([
          getOperatingCost(),
          getDeliverySuccessRate(),
        ]);
        setCostData(costRes);
        setRateData(rateRes);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return <div className="p-6 text-gray-500 animate-pulse">Đang phân tích chi phí...</div>;
  }

  if (error) {
    return (
      <div className="bg-red-50 text-red-600 p-4 rounded-lg border border-red-200 mt-6">
        <p className="font-semibold">Lỗi tải dữ liệu Analytics:</p>
        <p className="text-sm">{error}</p>
      </div>
    );
  }

  const formatVND = (num) => (num ? num.toLocaleString('vi-VN') + ' đ' : '0 đ');

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mt-8">
      <div className="mb-6">
        <h2 className="text-xl font-bold text-gray-800">Phân Tích Chi Phí & Hiệu Quả Giao Hàng</h2>
        <span className="text-xs text-gray-500">
          Ước tính tiêu hao năng lượng, tải trọng và tỷ lệ thành công nhiệm vụ
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {/* Tổng chi phí */}
        <div className="p-5 bg-indigo-50/50 border border-indigo-100 rounded-xl">
          <p className="text-xs font-semibold text-indigo-700 uppercase tracking-wider">
            Tổng Chi Phí Ước Tính
          </p>
          <p className="text-2xl font-black text-indigo-900 mt-2">
            {formatVND(costData?.estimated_total_cost_vnd)}
          </p>
          <p className="text-xs text-indigo-500 mt-1">Đơn vị: VNĐ</p>
        </div>

        {/* Chi phí trung bình / đơn */}
        <div className="p-5 bg-amber-50/50 border border-amber-100 rounded-xl">
          <p className="text-xs font-semibold text-amber-700 uppercase tracking-wider">
            Chi Phí TB / Đơn Hàng
          </p>
          <p className="text-2xl font-black text-amber-900 mt-2">
            {formatVND(costData?.average_cost_per_order_vnd)}
          </p>
          <p className="text-xs text-amber-500 mt-1">Chi phí cơ bản + phụ phí tải</p>
        </div>

        {/* Tổng khối lượng vận chuyển */}
        <div className="p-5 bg-emerald-50/50 border border-emerald-100 rounded-xl">
          <p className="text-xs font-semibold text-emerald-700 uppercase tracking-wider">
            Tổng Khối Lượng Hàng
          </p>
          <p className="text-2xl font-black text-emerald-900 mt-2">
            {costData?.total_package_weight_kg || 0} kg
          </p>
          <p className="text-xs text-emerald-500 mt-1">Khối lượng kiện hàng đã nhận</p>
        </div>
      </div>

      {/* Biểu đồ tiến độ tỷ lệ hoàn thành */}
      <div className="p-5 border border-gray-100 rounded-xl bg-gray-50">
        <h3 className="text-sm font-bold text-gray-700 mb-3">Hiệu Quả Hoàn Thành Giao Hàng</h3>
        <div className="flex items-center gap-4">
          <div className="flex-1">
            <div className="w-full bg-gray-200 h-4 rounded-full overflow-hidden flex">
              <div
                className="bg-green-500 h-4 transition-all duration-500"
                style={{ width: `${rateData?.success_rate_percent || 0}%` }}
                title={`Thành công: ${rateData?.success_rate_percent || 0}%`}
              ></div>
              <div
                className="bg-red-500 h-4 transition-all duration-500"
                style={{ width: `${rateData?.failure_rate_percent || 0}%` }}
                title={`Thất bại: ${rateData?.failure_rate_percent || 0}%`}
              ></div>
            </div>
          </div>
          <span className="text-sm font-bold text-gray-700 min-w-[70px]">
            {rateData?.success_rate_percent || 0}% Đạt
          </span>
        </div>
        <div className="flex gap-6 mt-3 text-xs text-gray-600 font-medium">
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-green-500 inline-block"></span>
            Tỷ lệ giao thành công: {rateData?.success_rate_percent || 0}%
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-red-500 inline-block"></span>
            Tỷ lệ sự cố / Thất bại: {rateData?.failure_rate_percent || 0}%
          </span>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsVisualization;