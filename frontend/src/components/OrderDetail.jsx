import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';

const OrderDetail = ({ orderId, onClose }) => {
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [socketStatus, setSocketStatus] = useState('Đang kết nối...');

  // 1. Tải thông tin ban đầu của đơn hàng
  useEffect(() => {
    const fetchOrderDetail = async () => {
      try {
        setLoading(true);
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';
        const res = await fetch(`${apiUrl}/api/orders/${orderId}`);
        if (!res.ok) throw new Error('Không tìm thấy thông tin đơn hàng');
        const data = await res.json();
        setOrder(data);
      } catch (err) {
        console.error('Lỗi lấy chi tiết đơn:', err);
      } finally {
        setLoading(false);
      }
    };

    if (orderId) fetchOrderDetail();
  }, [orderId]);

  // 2. Tích hợp SocketIO lắng nghe Realtime từ Backend
  useEffect(() => {
    if (!orderId) return;

    const socketUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';
    const socket = io(socketUrl, {
      transports: ['websocket', 'polling'],
    });

    // Kết nối và xin vào room của đơn hàng
    socket.on('connect', () => {
      setSocketStatus('Realtime đã bật');
      socket.emit('join_order_room', { order_id: Number(orderId) });
    });

    // Lắng nghe sự kiện đổi trạng thái từ backend
    socket.on('order_status_updated', (data) => {
      console.log('[SocketIO] Nhận dữ liệu realtime:', data);
      setOrder((prev) => {
        if (!prev) return prev;
        return {
          ...prev,
          status: data.status,
          failure_reason: data.failure_reason ?? prev.failure_reason,
          retry_count: data.retry_count ?? prev.retry_count,
        };
      });
    });

    socket.on('disconnect', () => {
      setSocketStatus('Mất kết nối');
    });

    return () => {
      socket.disconnect();
    };
  }, [orderId]);

  // Cấu hình màu badge trạng thái
  const getBadgeStyle = (status) => {
    switch (status) {
      case 'DELIVERED':
      case 'COMPLETED':
        return 'bg-emerald-100 text-emerald-700 border-emerald-300';
      case 'APPROVED':
        return 'bg-blue-100 text-blue-700 border-blue-300';
      case 'IN_TRANSIT':
        return 'bg-amber-100 text-amber-700 border-amber-300 animate-pulse';
      case 'FAILED':
      case 'REJECTED':
        return 'bg-rose-100 text-rose-700 border-rose-300';
      default:
        return 'bg-slate-100 text-slate-700 border-slate-300';
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-xs p-4">
      <div className="bg-white w-full max-w-lg rounded-2xl shadow-xl border border-slate-150 overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        {/* Header Modal */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100 bg-slate-50/50">
          <div>
            <h3 className="text-base font-bold text-slate-800">
              Chi Tiết Đơn Hàng #{orderId}
            </h3>
            <span className="text-xs text-emerald-600 flex items-center gap-1.5 mt-0.5">
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-ping"></span>
              {socketStatus}
            </span>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 p-1.5 rounded-lg hover:bg-slate-100 transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Nội dung chi tiết */}
        <div className="p-6">
          {loading ? (
            <div className="py-8 text-center text-slate-400 text-sm animate-pulse">
              Đang tải dữ liệu đơn hàng...
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex justify-between items-center p-3.5 bg-slate-50 rounded-xl border border-slate-200">
                <span className="text-xs font-semibold text-slate-500">TRẠNG THÁI HIỆN TẠI</span>
                <span
                  className={`text-xs font-bold px-3 py-1 rounded-full border transition-all duration-300 ${getBadgeStyle(
                    order?.status
                  )}`}
                >
                  {order?.status || 'PENDING'}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-150">
                  <span className="text-slate-400 block mb-1">Khách hàng:</span>
                  <span className="font-semibold text-slate-700">
                    {order?.customer_name || `Mã KH #${order?.customer_id || 'N/A'}`}
                  </span>
                </div>
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-150">
                  <span className="text-slate-400 block mb-1">Trọng lượng:</span>
                  <span className="font-semibold text-slate-700">
                    {order?.weight ? `${order.weight} kg` : 'Chưa cập nhật'}
                  </span>
                </div>
              </div>

              {/* Thông tin số lần thử lại nếu có retry */}
              {order?.retry_count > 0 && (
                <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-700">
                  <span className="font-bold">Số lần giao lại (Retry):</span> {order.retry_count} lần
                </div>
              )}

              {/* Lý do thất bại nếu đơn FAILED */}
              {order?.failure_reason && (
                <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-700">
                  <span className="font-bold">Lý do sự cố:</span> {order.failure_reason}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3.5 bg-slate-50 border-t border-slate-100 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-200 rounded-xl transition-all"
          >
            Đóng
          </button>
        </div>
      </div>
    </div>
  );
};

export default OrderDetail;