const API_BASE_URL = 'http://localhost:5000/api/analytics';

// Lấy tỷ lệ thành công và KPI tổng quan
export const getDeliverySuccessRate = async () => {
  const res = await fetch(`${API_BASE_URL}/success-rate`);
  if (!res.ok) throw new Error('Không thể lấy tỷ lệ giao hàng');
  return await res.json();
};

// Lấy phân bố trạng thái đơn hàng 
export const getOrdersByStatus = async () => {
  const res = await fetch(`${API_BASE_URL}/orders-by-status`);
  if (!res.ok) throw new Error('Không thể lấy thống kê trạng thái đơn');
  return await res.json();
};

// Lấy số lượng đơn xử lý theo trạm
export const getStationPerformance = async () => {
  const res = await fetch(`${API_BASE_URL}/station-performance`);
  if (!res.ok) throw new Error('Không thể lấy hiệu suất trạm');
  return await res.json();
};

// Lấy báo cáo chi phí vận hành & khối lượng
export const getOperatingCost = async () => {
  const res = await fetch(`${API_BASE_URL}/operating-cost`);
  if (!res.ok) throw new Error('Không thể lấy báo cáo chi phí vận hành');
  return await res.json();
};