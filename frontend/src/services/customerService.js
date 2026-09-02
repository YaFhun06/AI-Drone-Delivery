const API_BASE_URL = 'http://localhost:5000/api';

const MOCK_CUSTOMERS = [
  { id: 1, name: "Nguyễn Văn A", phone: "0901234567", email: "a.nguyen@gmail.com", address: "Quận 1, TP.HCM" },
  { id: 2, name: "Trần Thị B", phone: "0912345678", email: "b.tran@gmail.com", address: "Quận 3, TP.HCM" },
  { id: 3, name: "Lê Văn C", phone: "0987654321", email: "c.le@gmail.com", address: "TP. Thủ Đức" }
];

// Đã đổi tên thành fetchCustomers để khớp với CustomerList.jsx
export const fetchCustomers = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/customers`);
    if (!response.ok) throw new Error("Backend chưa sẵn sàng");
    
    const data = await response.json();
    return data.map(item => ({
      id: item.id,
      name: item.full_name || 'Chưa cập nhật tên',
      phone: item.phone || 'Chưa có SĐT',
      email: item.email || 'N/A',
      address: item.address_id ? `Địa chỉ ID #${item.address_id}` : 'Chưa có địa chỉ'
    }));
  } catch (error) {
    console.warn("Chưa kết nối được backend, chuyển sang mock data:", error.message);
    return MOCK_CUSTOMERS;
  }
};

export const getCustomerById = async (id) => {
  return MOCK_CUSTOMERS.find(c => c.id === parseInt(id)) || MOCK_CUSTOMERS[0];
};

export const createCustomer = async (data) => {
  console.log("Đã thêm khách hàng (Mock):", data);
  return { id: Math.floor(Math.random() * 1000), ...data };
};

export const updateCustomer = async (id, data) => {
  console.log("Đã sửa khách hàng (Mock):", id, data);
  return { id, ...data };
};

export const deleteCustomer = async (id) => {
  console.log("Đã xóa khách hàng (Mock):", id);
  return true;
};