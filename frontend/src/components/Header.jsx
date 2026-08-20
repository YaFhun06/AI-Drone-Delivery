import React from 'react';
import { Bell, User } from 'lucide-react';

const Header = () => {
  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6 sticky top-0 z-10">
      <div className="flex items-center gap-2">
        <h2 className="text-lg font-semibold text-gray-800">SmartDrone Delivery Portal</h2>
      </div>
      <div className="flex items-center gap-4">
        <button className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-full">
          <Bell size={20} />
        </button>
        <div className="flex items-center gap-2 border-l pl-4 border-gray-200">
          <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">
            <User size={18} />
          </div>
          <span className="text-sm font-medium text-gray-700">Admin</span>
        </div>
      </div>
    </header>
  );
};

export default Header;