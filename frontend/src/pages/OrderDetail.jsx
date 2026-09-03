import React, { useState, useEffect } from 'react';
import { getOrderById } from '../services/orderService';

const OrderDetail = ({ orderId = 1 }) => {
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchOrderDetail = async () => {
      try {
        setLoading(true);
        const data = await getOrderById(orderId);
        setOrder(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchOrderDetail();
  }, [orderId]);

  const trackingSteps = ['Đã tạo đơn', 'Đã gán trạm/drone', 'Đang vận chuyển', 'Giao thành công'];

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mt-8">
      <div className="flex justify-between items-center mb-6 pb-4 border-b border-gray-100">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Chi Tiết Đơn Hàng #{orderId}</h2>
          <p className="text-xs text-gray-500 mt-1">Thông tin vận chuyển và trạng thái tracking realtime</p>
        </div>
      </div>

      {loading && <p className="text-gray-500 animate-pulse mb-4">Đang tải thông tin chi tiết đơn hàng...</p>}

      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-md border border-red-200 mb-4">
          <p className="font-semibold">Lỗi tải dữ liệu chi tiết đơn hàng:</p>
          <p className="text-sm">Vui lòng chờ Backend khởi động ({error})</p>
        </div>
      )}

      {!loading && !error && order && (
        <div className="space-y-6">
          {/* Tracking Timeline */}
          <div>
            <h3 className="text-sm font-semibold text-gray-700 uppercase mb-3">Trạng thái vận chuyển</h3>
            <div className="grid grid-cols-4 gap-2 text-center text-xs">
              {trackingSteps.map((step, idx) => (
                <div
                  key={idx}
                  className={`p-2 rounded border font-medium ${
                    order.status_index >= idx
                      ? 'bg-blue-50 border-blue-200 text-blue-700'
                      : 'bg-gray-50 border-gray-200 text-gray-400'
                  }`}
                >
                  {step}
                </div>
              ))}
            </div>
          </div>

          {/* Chi tiết thông tin */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm bg-gray-50 p-4 rounded-lg">
            <div>
              <p className="text-gray-500">Khách hàng:</p>
              <p className="font-semibold text-gray-800">{order.customer_name || 'N/A'}</p>
            </div>
            <div>
              <p className="text-gray-500">Điểm giao nhận:</p>
              <p className="font-semibold text-gray-800">{order.destination || 'N/A'}</p>
            </div>
            <div>
              <p className="text-gray-500">Trạng thái hiện tại:</p>
              <span className="inline-block px-2 py-1 mt-1 rounded text-xs font-semibold bg-blue-100 text-blue-700">
                {order.status || 'Chờ xử lý'}
              </span>
            </div>
            <div>
              <p className="text-gray-500">Thời gian dự kiến (ETA):</p>
              <p className="font-semibold text-gray-800">{order.eta ? `${order.eta} phút` : '--'}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default OrderDetail;