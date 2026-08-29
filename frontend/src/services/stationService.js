export const fetchStations = async () => {
  // Mock data trạm đáp
  return [
    { id: 'ST-01', name: 'Trạm trung tâm Q1', status: 'Hoạt động', battery: '92%', dronesActive: 3 },
    { id: 'ST-02', name: 'Trạm Thủ Đức', status: 'Đang sạc', battery: '45%', dronesActive: 1 },
  ];
};