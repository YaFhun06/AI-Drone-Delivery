import DashboardCharts from './components/DashboardCharts';
import AnalyticsVisualization from './components/AnalyticsVisualization';
import React from 'react';
import Dashboard from './pages/Dashboard';
import OrderDetail from './pages/OrderDetail';
import CustomerList from './components/CustomerList';
import OrderList from './components/OrderList';
import StationList from './components/StationList';
import DroneList from './components/DroneList';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        <Dashboard />
        <DashboardCharts />
        <AnalyticsVisualization />
        <CustomerList />
        <OrderList />
        <OrderDetail orderId={1} />
        <StationList />
        <DroneList />
      </div>
    </div>
  );
}

export default App;