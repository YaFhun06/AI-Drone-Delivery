import React from 'react';
import { LayoutDashboard, Plane, MapPin, Package, Settings, LogOut } from 'lucide-react';

const Sidebar = () => {
  const menuItems = [
    { title: 'Dashboard', icon: <LayoutDashboard size={20} />, active: true },
    { title: 'Quản lý Drone', icon: <Plane size={20} /> },
    { title: 'Trạm hạ cánh', icon: <MapPin size={20} /> },
    { title: 'Đơn hàng & Kiện hàng', icon: <Package size={20} /> },
    { title: 'Cài đặt hệ thống', icon: <Settings size={20} /> },
  ];

  return (
    <aside className="w-64 bg-slate-900 text-slate-200 flex flex-col min-h-screen">
      <div className="p-5 border-b border-slate-800 flex items-center gap-3">
        <Plane className="text-blue-400" size={26} />
        <span className="font-bold text-lg text-white">SmartDrone</span>
      </div>
      
      <nav className="flex-1 p-4 space-y-1">
        {menuItems.map((item, index) => (
          <button
            key={index}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
              item.active 
                ? 'bg-blue-600 text-white' 
                : 'text-slate-400 hover:bg-slate-800 hover:text-white'
            }`}
          >
            {item.icon}
            {item.title}
          </button>
        ))}
      </nav>

      <div className="p-4 border-t border-slate-800">
        <button className="w-full flex items-center gap-3 px-4 py-2 text-sm text-red-400 hover:bg-slate-800 rounded-lg">
          <LogOut size={18} />
          Đăng xuất
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;