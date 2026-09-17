import React, { useState } from 'react';
import { authService } from '../services/authService';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [step, setStep] = useState(1);
  const [token, setToken] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleRequestReset = async (e) => {
    e.preventDefault();
    setError('');
    const res = await authService.forgotPassword(email);
    if (res.error) {
      setError(res.error);
    } else {
      setMessage('Mã xác nhận đã được gửi. Vui lòng kiểm tra console server (demo).');
      setStep(2);
    }
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    setError('');
    const res = await authService.resetPassword(token, newPassword);
    if (res.error) {
      setError(res.error);
    } else {
      setMessage('Đặt lại mật khẩu thành công! Vui lòng đăng nhập lại.');
      setStep(3);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <h1 className="text-2xl font-bold mb-6">Quên mật khẩu</h1>

        {error && <p className="text-red-500 mb-4">{error}</p>}
        {message && <p className="text-green-600 mb-4">{message}</p>}

        {step === 1 && (
          <form onSubmit={handleRequestReset}>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full p-2 border rounded mb-4"
              required
            />
            <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded">
              Gửi mã xác nhận
            </button>
          </form>
        )}

        {step === 2 && (
          <form onSubmit={handleResetPassword}>
            <input
              type="text"
              placeholder="Mã xác nhận"
              value={token}
              onChange={(e) => setToken(e.target.value)}
              className="w-full p-2 border rounded mb-4"
              required
            />
            <input
              type="password"
              placeholder="Mật khẩu mới"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              className="w-full p-2 border rounded mb-4"
              required
            />
            <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded">
              Đặt lại mật khẩu
            </button>
          </form>
        )}

        {step === 3 && (
          <a href="/login" className="block text-center text-blue-600 mt-4">
            Quay lại đăng nhập
          </a>
        )}
      </div>
    </div>
  );
};

export default ForgotPassword;