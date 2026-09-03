const API_BASE_URL = 'http://localhost:5000/api';

export const getOrders = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/orders`);
    if (!response.ok) {
      throw new Error(`Lỗi HTTP: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Lỗi kết nối API Orders:", error);
    throw error;
  }
};