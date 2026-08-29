import React from 'react';
import CustomerList from './components/CustomerList';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <CustomerList />
      </div>
    </div>
  );
}

export default App;