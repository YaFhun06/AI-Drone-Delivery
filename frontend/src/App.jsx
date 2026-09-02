import React from 'react';
import Dashboard from './pages/Dashboard'; // Import file Dashboard bạn vừa làm
import CustomerList from './components/CustomerList';
import OrderList from './components/OrderList';
import StationList from './components/StationList';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Thêm Dashboard vào trên cùng của trang */}
        <Dashboard />
        
        <CustomerList />
        <OrderList />
        <StationList />
      </div>
    </div>
  );
}

export default App;