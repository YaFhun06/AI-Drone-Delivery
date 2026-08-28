import React from 'react';
import MainLayout from './layouts/MainLayout';

function App() {
  return (
    <MainLayout>
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h1 className="text-2xl font-bold text-gray-800 mb-2">Xin chào!</h1>
        <p className="text-gray-600">Layout chung với Tailwind CSS đã hoạt động cực mượt.</p>
      </div>
    </MainLayout>
  );
}

export default App;