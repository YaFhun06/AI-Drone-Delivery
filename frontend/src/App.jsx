import React from 'react';
import CustomerList from './components/CustomerList';
import OrderList from './components/OrderList';
import StationList from './components/StationList';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        <CustomerList />
        <OrderList />
        <StationList />
      </div>
    </div>
  );
}

export default App;