const API_BASE_URL = 'http://localhost:5000/api';

export const getDrones = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/drones`);
    if (!response.ok) {
      throw new Error(`Lỗi HTTP: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Lỗi kết nối API Drones:', error);
    throw error;
  }
};

export const createDrone = async (droneData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/drones`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(droneData),
    });
    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.error || `Lỗi HTTP: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Lỗi tạo Drone:', error);
    throw error;
  }
};

export const deleteDrone = async (droneId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/drones/${droneId}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error(`Lỗi HTTP: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Lỗi xóa Drone #${droneId}:`, error);
    throw error;
  }
};