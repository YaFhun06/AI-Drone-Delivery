export const fetchOrders = async () => {
  // Mock data đơn hàng
  return [
    { id: 'ORD-001', customer: 'Nguyễn Văn A', status: 'Đang giao', destination: 'Quận 1', eta: '15 phút' },
    { id: 'ORD-002', customer: 'Trần Thị B', status: 'Hoàn thành', destination: 'Quận 3', eta: 'Đã giao' },
  ];
};