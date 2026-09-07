import React, { useState, useEffect } from 'react';
import { getOrders } from '../services/orderService';

const OrderList = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        setLoading(true);
        const data = await getOrders();
        setOrders(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, []);

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mt-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold text-gray-800">Quản Lý Đơn Hàng</h2>
        <span className="bg-orange-100 text-orange-800 text-sm font-semibold px-3 py-1 rounded-full">
          Tổng số: {orders.length} đơn
        </span>
      </div>

      {loading && <p className="text-gray-500 animate-pulse mb-4">Đang tải danh sách đơn hàng...</p>}
      
      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-md border border-red-200 mb-4">
          <p className="font-semibold">Lỗi tải dữ liệu đơn hàng:</p>
          <p className="text-sm">Vui lòng chờ Backend khởi động ({error})</p>
        </div>
      )}

      {!loading && !error && (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-gray-600">
            <thead className="bg-gray-50 text-gray-700 uppercase text-xs font-semibold">
              <tr>
                <th className="px-4 py-3 border-b">Mã Đơn</th>
                <th className="px-4 py-3 border-b">Khách Hàng</th>
                <th className="px-4 py-3 border-b">Điểm Đến</th>
                <th className="px-4 py-3 border-b">Trạng Thái</th>
                <th className="px-4 py-3 border-b">ETA</th>
              </tr>
            </thead>
            <tbody>
              {orders.length > 0 ? (
                orders.map((order, index) => (
                  <tr key={order.id || index} className="border-b hover:bg-gray-50">
                    <td className="px-4 py-3 font-medium text-blue-600">#{order.id}</td>
                    <td className="px-4 py-3">{order.customer_name || 'N/A'}</td>
                    <td className="px-4 py-3">{order.destination || 'N/A'}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        order.status === 'Completed' ? 'bg-green-100 text-green-700' : 
                        order.status === 'Pending' ? 'bg-yellow-100 text-yellow-700' : 'bg-blue-100 text-blue-700'
                      }`}>
                        {order.status || 'Unknown'}
                      </span>
                    </td>
                    <td className="px-4 py-3">{order.eta || '--'} phút</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5" className="px-4 py-8 text-center text-gray-500">
                    Chưa có đơn hàng nào trong hệ thống.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default OrderList;