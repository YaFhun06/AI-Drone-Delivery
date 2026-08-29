export const fetchCustomers = async () => {
  // Mock data khách hàng
  return [
    { id: 1, name: 'Nguyễn Văn A', email: 'a.nguyen@gmail.com', phone: '0901234567', address: 'Quận 1, TP.HCM' },
    { id: 2, name: 'Trần Thị B', email: 'b.tran@gmail.com', phone: '0912345678', address: 'Quận 3, TP.HCM' },
    { id: 3, name: 'Lê Văn C', email: 'c.le@gmail.com', phone: '0987654321', address: 'TP. Thủ Đức' },
  ];
};