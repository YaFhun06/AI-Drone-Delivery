import { useEffect, useMemo, useState } from 'react';
import {
  Bell, ChevronDown, ChevronRight, CircleHelp, Download, Ellipsis,
  Filter, LayoutDashboard, LogOut, MapPin, Menu, PackageCheck, Plus,
  Search, Settings, ShieldCheck, SlidersHorizontal, Truck, UserRound,
  UsersRound, X,
} from 'lucide-react';
import './App.css';
import DashboardCharts from './components/DashboardCharts';
import AnalyticsVisualization from './components/AnalyticsVisualization';
import OrderDetail from './components/OrderDetail';

const navItems = [
  { id: 'overview', label: 'Tổng quan', icon: LayoutDashboard },
  { id: 'users', label: 'Quản lý người dùng', icon: UsersRound },
  { id: 'customers', label: 'Quản lý khách hàng', icon: UserRound },
  { id: 'deliveries', label: 'Đơn giao hàng', icon: Truck },
];

const API_URL = 'http://localhost:5000';

async function apiFetch(path) {
  const token = localStorage.getItem('smartdrone_token');

  if (!token) {
    throw new Error('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.');
  }

  const response = await fetch(`${API_URL}${path}`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const message = String(data.msg || data.error || data.message || '').toLowerCase();
    const isInvalidToken =
      response.status === 401 ||
      (response.status === 422 &&
        (message.includes('signature') ||
          message.includes('token') ||
          message.includes('jwt')));

    if (isInvalidToken) {
      localStorage.removeItem('smartdrone_token');
      localStorage.removeItem('smartdrone_user');
      throw new Error('Token đăng nhập không hợp lệ hoặc đã hết hạn. Vui lòng đăng nhập lại.');
    }

    throw new Error(
      data.error ||
        data.message ||
        data.msg ||
        `HTTP ${response.status}`
    );
  }

  return data;
}

function Avatar({ initials, color = 'blue' }) { return <span className={`avatar avatar-${color}`}>{initials}</span>; }
function StatusPill({ children, tone = 'blue' }) { return <span className={`status status-${tone}`}><span className="status-dot" />{children}</span>; }
function Header({ title, onMenu, onHelp, user, onLogout }) { return <header className="topbar"><button className="mobile-menu icon-button" onClick={onMenu} aria-label="Mở menu"><Menu size={20} /></button><div className="breadcrumbs"><span>Workspace</span><ChevronRight size={15} /><strong>{title}</strong></div><div className="top-actions"><button className="icon-button" onClick={onHelp} aria-label="Trợ giúp"><CircleHelp size={19} /></button><button className="notification icon-button" aria-label="Thông báo"><Bell size={19} /><span /></button><button className="profile profile-button" onClick={onLogout} title="Đăng xuất"><Avatar initials={(user?.full_name || 'NA').split(' ').map((part) => part[0]).slice(-2).join('')} color="coral" /><span><b>{user?.full_name || user?.email || 'Người dùng'}</b><small>Đăng xuất</small></span><LogOut size={16} /></button></div></header>; }
function Sidebar({ active, setActive, open, onLogout }) { return <aside className={`sidebar ${open ? 'sidebar-open' : ''}`}><div className="brand"><span className="brand-mark"><PackageCheck size={21} /></span><span>smart<span>drone</span></span></div><div className="workspace-switch"><span className="workspace-dot" /><span><small>Workspace hiện tại</small><b>Vận hành giao hàng</b></span><ChevronDown size={15} /></div><div className="nav-label">QUẢN LÝ VẬN HÀNH</div><nav>{navItems.map(({ id, label, icon: Icon }) => <button key={id} className={`nav-item ${active === id ? 'active' : ''}`} onClick={() => setActive(id)}><Icon size={18} /><span>{label}</span>{id === 'deliveries' && <span className="nav-count">24</span>}</button>)}</nav><div className="nav-label nav-label-secondary">HỆ THỐNG</div><nav><button className="nav-item"><Settings size={18} /><span>Cài đặt</span></button><button className="nav-item"><ShieldCheck size={18} /><span>Nhật ký hoạt động</span></button></nav><div className="sidebar-bottom"><div className="help-card"><div className="help-icon"><CircleHelp size={18} /></div><b>Cần hỗ trợ?</b><p>Đội vận hành luôn sẵn sàng.</p><button onClick={() => window.alert('Đã gửi yêu cầu hỗ trợ.')}>Liên hệ hỗ trợ <ChevronRight size={14} /></button></div><button className="logout" onClick={onLogout}><LogOut size={17} /> Đăng xuất</button><small className="version">SmartDrone v1.0.0</small></div></aside>; }
function StatCard({ label, value, detail, icon: Icon, tone, trend }) { return <div className="stat-card"><div className={`stat-icon stat-${tone}`}><Icon size={19} /></div><div className="stat-copy"><span>{label}</span><strong>{value}</strong><small className={trend ? 'positive' : ''}>{trend && <b>{trend}</b>} {detail}</small></div></div>; }
function Toolbar({ search, setSearch, placeholder, onAdd, addLabel }) { return <div className="toolbar"><div className="search-box"><Search size={17} /><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder={placeholder} /></div><button className="filter-button"><Filter size={16} /> Bộ lọc <ChevronDown size={15} /></button><button className="filter-button filter-icon"><SlidersHorizontal size={16} /></button>{onAdd && <button className="primary-button" onClick={onAdd}><Plus size={17} /> {addLabel}</button>}</div>; }
function PageHeading({ eyebrow, title, description, buttonLabel, onAdd }) { return <div className="page-intro module-heading"><div><p className="eyebrow">{eyebrow}</p><h1>{title}</h1><p className="muted">{description}</p></div><button className="primary-button" onClick={onAdd}><Plus size={17} /> {buttonLabel}</button></div>; }
function Pagination({ count }) { return <div className="pagination"><span>1–{count} trên {count} kết quả</span><div><button disabled>Trước</button><button className="current-page">1</button><button disabled>Sau</button></div></div>; }
// eslint-disable-next-line no-unused-vars
function Overview({ setActive }) { return null; }

function DeliveryTable({ rows, compact = false, onSelect }) { 
  return (
    <div className="table-wrap">
      <table className={compact ? 'compact-table' : ''}>
        <thead>
          <tr>
            <th>Mã đơn</th>
            <th>Khách hàng</th>
            <th>Lộ trình</th>
            <th>Trạng thái</th>
            <th>Tiến độ</th>
            <th>{!compact && 'Drone'}</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id} className="clickable-row" onClick={() => onSelect?.(row)}>
              <td><b className="order-id">{row.id}</b><small className="table-sub">Hôm nay, 09:42</small></td>
              <td><div className="customer-inline"><Avatar initials={(row.customer || 'KH').split(' ').map((word) => word[0]).slice(-2).join('')} color={row.color} /><b>{row.customer}</b></div></td>
              <td className="muted-cell"><span className="route"><MapPin size={14} />{row.route}</span></td>
              <td><StatusPill tone={row.color === 'green' ? 'green' : row.color === 'amber' ? 'amber' : row.color === 'purple' ? 'purple' : 'blue'}>{row.status}</StatusPill></td>
              <td><div className="progress-cell"><div className="progress-track"><span style={{ width: `${row.progress}%` }} className={`progress-${row.color}`} /></div><small>{row.progress}%</small></div></td>
              {!compact && <td><span className="drone-tag"><Truck size={14} /> {row.drone}</span></td>}
              <td><button className="more-button" aria-label={`Xem ${row.id}`} onClick={(e) => { e.stopPropagation(); onSelect?.(row); }}><Ellipsis size={19} /></button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  ); 
}

function DetailDrawer({ item, type, onClose }) { 
  if (!item) return null; 
  const customer = type === 'customer'; 
  return (
    <div className="drawer-backdrop" onClick={onClose}>
      <aside className="detail-drawer" onClick={(event) => event.stopPropagation()}>
        <div className="drawer-header">
          <span>CHI TIẾT {customer ? 'KHÁCH HÀNG' : 'ĐƠN GIAO HÀNG'}</span>
          <button className="icon-button" onClick={onClose} aria-label="Đóng"><X size={19} /></button>
        </div>
        <div className="drawer-profile">
          {customer ? (
            <>
              <Avatar initials={item.initials} color={item.color} />
              <h2>{item.name}</h2>
              <p>{item.email}</p>
              <StatusPill tone="green">Đang hoạt động</StatusPill>
            </>
          ) : (
            <>
              <div className="drawer-order-icon"><Truck size={25} /></div>
              <h2>{item.id}</h2>
              <p>{item.customer}</p>
              <StatusPill tone="blue">{item.status}</StatusPill>
            </>
          )}
        </div>
        <div className="drawer-section">
          <h3>{customer ? 'Thông tin tổng quan' : 'Thông tin chuyến giao'}</h3>
          {customer ? (
            <>
              <div className="detail-row"><span>Số điện thoại</span><b>{item.phone}</b></div>
              <div className="detail-row"><span>Ngày tham gia</span><b>{item.joined}</b></div>
              <div className="detail-row"><span>Tổng đơn hàng</span><b>{item.orders} đơn</b></div>
              <div className="detail-row"><span>Tổng chi tiêu</span><b>{item.spent}</b></div>
            </>
          ) : (
            <>
              <div className="detail-row"><span>Lộ trình</span><b>{item.route}</b></div>
              <div className="detail-row"><span>Drone phụ trách</span><b>{item.drone}</b></div>
              <div className="detail-row"><span>Thời gian dự kiến</span><b>{item.eta}</b></div>
              <div className="detail-row"><span>Tiến độ</span><b>{item.progress}%</b></div>
            </>
          )}
        </div>
        <button className="primary-button drawer-action">
          {customer ? 'Xem lịch sử đơn hàng' : 'Mở bản đồ theo dõi'} <ChevronRight size={16} />
        </button>
      </aside>
    </div>
  ); 
}

function LiveUserPage({ onAdd }) {
  const [rows, setRows] = useState([]);
  const [search, setSearch] = useState('');
  const [state, setState] = useState({ loading: true, error: '' });
  useEffect(() => {
    apiFetch('/api/users')
      .then((data) => {
        const users = Array.isArray(data) ? data : data.users || [];
        setRows(users);
      })
      .catch((error) => setState({ loading: false, error: error.message }))
      .finally(() => setState((current) => ({ ...current, loading: false })));
  }, []);
  const filtered = useMemo(() => rows.filter((row) => `${row.full_name} ${row.email} ${row.role}`.toLowerCase().includes(search.toLowerCase())), [rows, search]);
  return <><PageHeading eyebrow="QUẢN LÝ HỆ THỐNG" title="Quản lý người dùng" description="Dữ liệu tài khoản được tải trực tiếp từ Supabase qua Backend." buttonLabel="Thêm người dùng" onAdd={onAdd} /><section className="panel table-panel"><Toolbar search={search} setSearch={setSearch} placeholder="Tìm theo tên, email hoặc vai trò..." onAdd={onAdd} addLabel="Thêm người dùng" />{state.loading && <div className="data-state">Đang tải người dùng từ Supabase...</div>}{state.error && <div className="data-state data-error">{state.error}</div>}{!state.loading && !state.error && <><div className="table-meta"><span>{filtered.length} người dùng từ cơ sở dữ liệu</span><button className="export-button"><Download size={15} /> Xuất danh sách</button></div><div className="table-wrap"><table><thead><tr><th>Người dùng</th><th>Vai trò</th><th>Trạng thái</th><th>Ngày tạo</th><th /></tr></thead><tbody>{filtered.map((row) => <tr key={row.id}><td><div className="person-cell"><Avatar initials={(row.full_name || row.email).split(' ').map((part) => part[0]).slice(-2).join('')} color="blue" /><span><b>{row.full_name || 'Chưa cập nhật'}</b><small>{row.email}</small></span></div></td><td><span className="role-label">{row.role}</span></td><td><StatusPill tone={row.is_active ? 'green' : 'red'}>{row.is_active ? 'Đang hoạt động' : 'Đã khóa'}</StatusPill></td><td className="muted-cell">{row.created_at ? new Date(row.created_at).toLocaleDateString('vi-VN') : '—'}</td><td><button className="more-button" aria-label={`Tùy chọn ${row.email}`}><Ellipsis size={19} /></button></td></tr>)}</tbody></table></div><Pagination count={filtered.length} /></>}</section></>;
}

function LiveCustomerPage({ onAdd, onSelect }) {
  const [rows, setRows] = useState([]);
  const [search, setSearch] = useState('');
  const [state, setState] = useState({ loading: true, error: '' });
  useEffect(() => {
    apiFetch('/api/customers')
      .then((data) => {
        const customers = Array.isArray(data) ? data : data.customers || [];
        setRows(customers.map((row) => ({
          ...row,
          name: row.full_name || 'Chưa cập nhật',
          email: row.email || `customer-${row.id}@smartdrone.vn`,
          orders: row.orders || 0,
          spent: row.spent || '—',
          status: row.is_active === false ? 'Đã khóa' : 'Hoạt động',
          initials: (row.full_name || 'KH').split(' ').map((part) => part[0]).slice(-2).join(''),
          color: 'blue',
        })));
      })
      .catch((error) => setState({ loading: false, error: error.message }))
      .finally(() => setState((current) => ({ ...current, loading: false })));
  }, []);
  const filtered = useMemo(() => rows.filter((row) => `${row.name} ${row.email} ${row.phone}`.toLowerCase().includes(search.toLowerCase())), [rows, search]);
  return <><PageHeading eyebrow="QUẢN LÝ KHÁCH HÀNG" title="Khách hàng" description="Dữ liệu khách hàng được tải trực tiếp từ Supabase qua Backend." buttonLabel="Thêm khách hàng" onAdd={onAdd} /><section className="panel table-panel"><Toolbar search={search} setSearch={setSearch} placeholder="Tìm theo tên hoặc số điện thoại..." onAdd={onAdd} addLabel="Thêm khách hàng" />{state.loading && <div className="data-state">Đang tải khách hàng từ Supabase...</div>}{state.error && <div className="data-state data-error">{state.error}</div>}{!state.loading && !state.error && <><div className="table-meta"><span>{filtered.length} khách hàng từ cơ sở dữ liệu</span><button className="export-button"><Download size={15} /> Xuất danh sách</button></div><div className="table-wrap"><table><thead><tr><th>Khách hàng</th><th>Số điện thoại</th><th>Mã địa chỉ</th><th>Trạng thái</th><th /></tr></thead><tbody>{filtered.map((row) => <tr key={row.id} onClick={() => onSelect(row)} className="clickable-row"><td><div className="person-cell"><Avatar initials={row.initials} color={row.color} /><span><b>{row.name}</b><small>{row.email}</small></span></div></td><td className="muted-cell">{row.phone || '—'}</td><td className="muted-cell">{row.address_id || '—'}</td><td><StatusPill tone="green">{row.status}</StatusPill></td><td><button className="more-button" aria-label={`Tùy chọn ${row.name}`} onClick={(event) => event.stopPropagation()}><Ellipsis size={19} /></button></td></tr>)}</tbody></table></div><Pagination count={filtered.length} /></>}</section></>;
}

function LiveDeliveryPage({ onSelect }) {
  const [rows, setRows] = useState([]);
  const [state, setState] = useState({ loading: true, error: '' });
  useEffect(() => {
    apiFetch('/api/orders')
      .then((data) => {
        const orders = Array.isArray(data) ? data : data.orders || [];
        setRows(orders.map((row) => ({
          ...row,
          id: row.id || row.order_id || '—',
          customer: row.customer_name || 'Chưa có tên',
          route: `Trạm #${row.station_id || 'chưa gán'}`,
          eta: row.scheduled_time ? new Date(row.scheduled_time).toLocaleString('vi-VN') : '—',
          drone: row.drone_name || 'Chưa gán',
          progress: row.status === 'COMPLETED' ? 100 : row.status === 'PENDING' ? 10 : 50,
          color: row.status === 'COMPLETED' ? 'green' : row.status === 'PENDING' ? 'amber' : 'blue',
        })));
      })
      .catch((error) => setState({ loading: false, error: error.message }))
      .finally(() => setState((current) => ({ ...current, loading: false })));
  }, []);
  return <><PageHeading eyebrow="QUẢN LÝ GIAO HÀNG" title="Đơn giao hàng" description="Đơn hàng được tải trực tiếp từ Supabase qua Backend." buttonLabel="Tạo đơn giao" onAdd={() => window.alert('Chức năng tạo đơn sẽ kết nối API tiếp theo.')} /><section className="panel table-panel"><div className="delivery-toolbar"><div className="search-box"><Search size={17} /><input placeholder="Tìm mã đơn hoặc tên khách hàng..." /></div><button className="filter-button"><Filter size={16} /> Tất cả trạng thái <ChevronDown size={15} /></button></div>{state.loading && <div className="data-state">Đang tải đơn giao hàng từ Supabase...</div>}{state.error && <div className="data-state data-error">{state.error}</div>}{!state.loading && !state.error && <DeliveryTable rows={rows} onSelect={onSelect} />}</section></>;
}

function LiveOverview({ setActive, onSelectOrder }) {
  const [data, setData] = useState({ users: [], customers: [], orders: [] });
  const [state, setState] = useState({ loading: true, error: '' });
  useEffect(() => {
    Promise.all([
      apiFetch('/api/users'),
      apiFetch('/api/customers'),
      apiFetch('/api/orders'),
    ])
      .then(([usersData, customersData, ordersData]) => {
        setData({
          users: Array.isArray(usersData) ? usersData : usersData.users || [],
          customers: Array.isArray(customersData) ? customersData : customersData.customers || [],
          orders: Array.isArray(ordersData) ? ordersData : ordersData.orders || [],
        });
      })
      .catch((error) => setState({ loading: false, error: error.message }))
      .finally(() => setState((current) => ({ ...current, loading: false })));
  }, []);
  const activeOrders = data.orders.filter((order) => !['COMPLETED', 'REJECTED', 'FAILED'].includes(order.status)).length;
<<<<<<< HEAD
  return <><div className="page-intro"><div><p className="eyebrow">DỮ LIỆU TRỰC TIẾP TỪ SUPABASE</p><h1>Chào buổi sáng</h1><p className="muted">Các chỉ số dưới đây được đọc từ cơ sở dữ liệu qua Backend.</p></div><button className="outline-button" onClick={() => setActive('deliveries')}><Truck size={16} /> Theo dõi đơn hàng</button></div>{state.loading && <div className="data-state">Đang đồng bộ dữ liệu từ Supabase...</div>}{state.error && <div className="data-state data-error">{state.error}</div>}{!state.loading && !state.error && <><div className="stat-grid"><StatCard label="Tổng người dùng" value={data.users.length} detail="tài khoản trong hệ thống" icon={UsersRound} tone="blue" /><StatCard label="Khách hàng" value={data.customers.length} detail="hồ sơ khách hàng" icon={UserRound} tone="coral" /><StatCard label="Tổng đơn giao" value={data.orders.length} detail="đơn trong cơ sở dữ liệu" icon={Truck} tone="green" /><StatCard label="Đang xử lý" value={activeOrders} detail="đơn chưa hoàn tất" icon={MapPin} tone="purple" /></div><div className="overview-grid"><section className="panel quick-panel"><div className="panel-heading"><div><h2>Thao tác nhanh</h2><p>Truy cập các module dùng dữ liệu thật</p></div></div><button onClick={() => setActive('users')} className="quick-action"><span className="quick-icon blue-bg"><UsersRound size={18} /></span><span><b>Quản lý người dùng</b><small>{data.users.length} tài khoản đã tải</small></span><ChevronRight size={17} /></button><button onClick={() => setActive('customers')} className="quick-action"><span className="quick-icon coral-bg"><UserRound size={18} /></span><span><b>Quản lý khách hàng</b><small>{data.customers.length} khách hàng đã tải</small></span><ChevronRight size={17} /></button><button onClick={() => setActive('deliveries')} className="quick-action"><span className="quick-icon green-bg"><Truck size={18} /></span><span><b>Theo dõi giao hàng</b><small>{activeOrders} đơn đang xử lý</small></span><ChevronRight size={17} /></button></section><section className="panel quick-panel"><div className="panel-heading"><div><h2>Trạng thái đồng bộ</h2><p>Kết nối Backend và Supabase</p></div></div><div className="sync-status"><span className="sync-pulse" /><b>Đang hoạt động</b><small>Backend đã kết nối cơ sở dữ liệu</small></div><div className="sync-detail"><span>Người dùng</span><b>{data.users.length} bản ghi</b></div><div className="sync-detail"><span>Khách hàng</span><b>{data.customers.length} bản ghi</b></div><div className="sync-detail"><span>Đơn giao hàng</span><b>{data.orders.length} bản ghi</b></div></section></div><section className="panel recent-panel"><div className="panel-heading"><div><h2>Đơn giao hàng gần đây</h2><p>Dữ liệu mới nhất từ Supabase</p></div><button className="text-button" onClick={() => setActive('deliveries')}>Xem tất cả <ChevronRight size={15} /></button></div><DeliveryTable rows={data.orders.slice(0, 5).map((row) => ({ ...row, customer: row.customer_name || row.customer?.full_name || row.customer?.name || 'Chưa có tên', route: `Trạm #${row.station_id || 'chưa gán'}`, status: row.status, eta: row.scheduled_time || '—', drone: 'Chưa gán', progress: row.status === 'COMPLETED' ? 100 : 40, color: row.status === 'COMPLETED' ? 'green' : 'blue' }))} compact /></section></>}</>;
=======

  return (
    <>
      <div className="page-intro">
        <div>
          <p className="eyebrow">DỮ LIỆU TRỰC TIẾP TỪ SUPABASE</p>
          <h1>Chào buổi sáng</h1>
          <p className="muted">Các chỉ số dưới đây được đọc từ cơ sở dữ liệu qua Backend.</p>
        </div>
        <button className="outline-button" onClick={() => setActive('deliveries')}>
          <Truck size={16} /> Theo dõi đơn hàng
        </button>
      </div>

      {state.loading && <div className="data-state">Đang đồng bộ dữ liệu từ Supabase...</div>}
      {state.error && <div className="data-state data-error">{state.error}</div>}

      {!state.loading && !state.error && (
        <>
          <div className="stat-grid">
            <StatCard label="Tổng người dùng" value={data.users.length} detail="tài khoản trong hệ thống" icon={UsersRound} tone="blue" />
            <StatCard label="Khách hàng" value={data.customers.length} detail="hồ sơ khách hàng" icon={UserRound} tone="coral" />
            <StatCard label="Tổng đơn giao" value={data.orders.length} detail="đơn trong cơ sở dữ liệu" icon={Truck} tone="green" />
            <StatCard label="Đang xử lý" value={activeOrders} detail="đơn chưa hoàn tất" icon={MapPin} tone="purple" />
          </div>

          <div className="overview-grid">
            <section className="panel quick-panel">
              <div className="panel-heading">
                <div><h2>Thao tác nhanh</h2><p>Truy cập các module dùng dữ liệu thật</p></div>
              </div>
              <button onClick={() => setActive('users')} className="quick-action">
                <span className="quick-icon blue-bg"><UsersRound size={18} /></span>
                <span><b>Quản lý người dùng</b><small>{data.users.length} tài khoản đã tải</small></span>
                <ChevronRight size={17} />
              </button>
              <button onClick={() => setActive('customers')} className="quick-action">
                <span className="quick-icon coral-bg"><UserRound size={18} /></span>
                <span><b>Quản lý khách hàng</b><small>{data.customers.length} khách hàng đã tải</small></span>
                <ChevronRight size={17} />
              </button>
              <button onClick={() => setActive('deliveries')} className="quick-action">
                <span className="quick-icon green-bg"><Truck size={18} /></span>
                <span><b>Theo dõi giao hàng</b><small>{activeOrders} đơn đang xử lý</small></span>
                <ChevronRight size={17} />
              </button>
            </section>

            <section className="panel quick-panel">
              <div className="panel-heading">
                <div><h2>Trạng thái đồng bộ</h2><p>Kết nối Backend và Supabase</p></div>
              </div>
              <div className="sync-status"><span className="sync-pulse" /><b>Đang hoạt động</b><small>Backend đã kết nối cơ sở dữ liệu</small></div>
              <div className="sync-detail"><span>Người dùng</span><b>{data.users.length} bản ghi</b></div>
              <div className="sync-detail"><span>Khách hàng</span><b>{data.customers.length} bản ghi</b></div>
              <div className="sync-detail"><span>Đơn giao hàng</span><b>{data.orders.length} bản ghi</b></div>
            </section>
          </div>

          <section className="panel recent-panel">
            <div className="panel-heading">
              <div><h2>Đơn giao hàng gần đây</h2><p>Dữ liệu mới nhất từ Supabase</p></div>
              <button className="text-button" onClick={() => setActive('deliveries')}>
                Xem tất cả <ChevronRight size={15} />
              </button>
            </div>
            <DeliveryTable
              rows={data.orders.slice(0, 5).map((row) => ({
                ...row,
                customer: row.customer_name,
                route: `Trạm #${row.station_id || 'chưa gán'}`,
                status: row.status,
                eta: row.scheduled_time || '—',
                drone: 'Chưa gán',
                progress: row.status === 'COMPLETED' ? 100 : 40,
                color: row.status === 'COMPLETED' ? 'green' : 'blue',
              }))}
              compact
              onSelect={onSelectOrder}
            />
          </section>

          <div className="mt-8 space-y-6">
            <DashboardCharts />
            <AnalyticsVisualization />
          </div>
        </>
      )}
    </>
  );
>>>>>>> 082831a7eb1633bcd8785454fe60ddc1c387e678
}

function Login({ onLogin, onGoToRegister }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const submit = async (event) => {
    event.preventDefault();
    setError('');
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.error || data.message || data.msg || 'Email hoặc mật khẩu không đúng.');
      }
      onLogin(data);
    } catch (requestError) {
      setError(requestError.message || 'Không thể kết nối đến máy chủ.');
    } finally {
      setLoading(false);
    }
  };
  return <main className="login-shell"><div className="login-decoration"><div className="login-orbit orbit-one" /><div className="login-orbit orbit-two" /><div className="login-drone"><PackageCheck size={34} /></div><p>Smart delivery, <b>made simple.</b></p></div><section className="login-card"><div className="login-brand"><span className="brand-mark"><PackageCheck size={21} /></span><span>smart<span>drone</span></span></div><div className="login-heading"><p className="eyebrow">WORKSPACE VẬN HÀNH</p><h1>Chào mừng trở lại</h1><p>Đăng nhập để tiếp tục quản lý hệ thống giao hàng.</p></div><form onSubmit={submit}><label>Email hoặc số điện thoại<input type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="you@smartdrone.vn" autoComplete="email" required /></label><label>Mật khẩu<div className="password-field"><input type="password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="Nhập mật khẩu của bạn" autoComplete="current-password" required /></div></label>{error && <div className="login-error">{error}</div>}<div className="login-options"><label className="remember"><input type="checkbox" /> Ghi nhớ đăng nhập</label><button type="button" onClick={() => setError('Vui lòng liên hệ quản trị viên để đặt lại mật khẩu.')}>Quên mật khẩu?</button></div><div className="login-options"><button type="button" onClick={onGoToRegister}>Chưa có tài khoản? Đăng ký</button></div><button className="primary-button login-submit" type="submit" disabled={loading}>{loading ? 'Đang xác thực...' : 'Đăng nhập'} {!loading && <ChevronRight size={17} />}</button></form><p className="login-footer">© 2026 SmartDrone Delivery</p></section></main>;
}

function Register({ onRegistered, onBackToLogin }) {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const submit = async (event) => {
    event.preventDefault();
    setError('');
    if (password !== confirmPassword) {
      setError('Mật khẩu xác nhận không khớp.');
      return;
    }
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ full_name: fullName, email, phone, password }),
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.error || data.message || data.msg || 'Đăng ký thất bại.');
      }
      onRegistered(data);
    } catch (requestError) {
      setError(requestError.message || 'Không thể kết nối đến máy chủ.');
    } finally {
      setLoading(false);
    }
  };

  return <main className="login-shell"><div className="login-decoration"><div className="login-orbit orbit-one" /><div className="login-orbit orbit-two" /><div className="login-drone"><PackageCheck size={34} /></div><p>Smart delivery, <b>made simple.</b></p></div><section className="login-card"><div className="login-brand"><span className="brand-mark"><PackageCheck size={21} /></span><span>smart<span>drone</span></span></div><div className="login-heading"><p className="eyebrow">WORKSPACE VẬN HÀNH</p><h1>Tạo tài khoản mới</h1><p>Đăng ký để bắt đầu sử dụng hệ thống giao hàng.</p></div><form onSubmit={submit}><label>Họ và tên<input type="text" value={fullName} onChange={(event) => setFullName(event.target.value)} placeholder="Nguyễn Văn A" required /></label><label>Email<input type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="you@smartdrone.vn" autoComplete="email" required /></label><label>Số điện thoại<input type="tel" value={phone} onChange={(event) => setPhone(event.target.value)} placeholder="09xxxxxxxx" required /></label><label>Mật khẩu<div className="password-field"><input type="password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="Tạo mật khẩu" autoComplete="new-password" required /></div></label><label>Xác nhận mật khẩu<div className="password-field"><input type="password" value={confirmPassword} onChange={(event) => setConfirmPassword(event.target.value)} placeholder="Nhập lại mật khẩu" autoComplete="new-password" required /></div></label>{error && <div className="login-error">{error}</div>}<button className="primary-button login-submit" type="submit" disabled={loading}>{loading ? 'Đang tạo tài khoản...' : 'Đăng ký'} {!loading && <ChevronRight size={17} />}</button></form><div className="login-options"><button type="button" onClick={onBackToLogin}>Đã có tài khoản? Đăng nhập</button></div><p className="login-footer">© 2026 SmartDrone Delivery</p></section></main>;
}

function App() {
  const [active, setActive] = useState('overview');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [detail, setDetail] = useState(null);
  const [toast, setToast] = useState(false);
  const [authView, setAuthView] = useState('login');
  const [user, setUser] = useState(() => { try { return JSON.parse(localStorage.getItem('smartdrone_user')) || null; } catch { return null; } });
  const title = navItems.find((item) => item.id === active)?.label || 'Tổng quan';
  const add = () => { setToast(true); window.setTimeout(() => setToast(false), 2400); };
  
  const handleLogin = (data) => { 
    localStorage.setItem('smartdrone_token', data.access_token); 
    localStorage.setItem('smartdrone_user', JSON.stringify(data.user)); 
    setUser(data.user); 
  };
  
  const handleLogout = async () => {
    const token = localStorage.getItem('smartdrone_token');
    try {
      if (token) await fetch(`${API_URL}/api/auth/logout`, { method: 'POST', headers: { Authorization: `Bearer ${token}` } });
    } finally {
      localStorage.removeItem('smartdrone_token');
      localStorage.removeItem('smartdrone_user');
      setUser(null);
      setDetail(null);
    }
  };

  if (!user) {
    return authView === 'register'
      ? <Register onRegistered={handleLogin} onBackToLogin={() => setAuthView('login')} />
      : <Login onLogin={handleLogin} onGoToRegister={() => setAuthView('register')} />;
  }

  return (
    <div className="app-shell">
      <Sidebar active={active} setActive={(id) => { setActive(id); setSidebarOpen(false); }} open={sidebarOpen} onLogout={handleLogout} />
      <main className="main-area">
        <Header title={title} onMenu={() => setSidebarOpen((open) => !open)} onHelp={add} user={user} onLogout={handleLogout} />
        <div className="content">
          {active === 'overview' && (
            <LiveOverview 
              setActive={setActive} 
              onSelectOrder={(item) => setDetail({ item, type: 'delivery' })} 
            />
          )}
          {active === 'users' && <LiveUserPage onAdd={add} />}
          {active === 'customers' && <LiveCustomerPage onAdd={add} onSelect={(item) => setDetail({ item, type: 'customer' })} />}
          {active === 'deliveries' && <LiveDeliveryPage onSelect={(item) => setDetail({ item, type: 'delivery' })} />}
        </div>
      </main>

      {/* Chi tiết khách hàng giữ nguyên DetailDrawer */}
      {detail && detail.type === 'customer' && (
        <DetailDrawer {...detail} onClose={() => setDetail(null)} />
      )}

      {/* Chi tiết đơn hàng kích hoạt OrderDetail với Socket.IO Realtime */}
      {detail && detail.type === 'delivery' && (
        <OrderDetail 
          orderId={detail.item.id} 
          onClose={() => setDetail(null)} 
        />
      )}

      {toast && <div className="toast"><PackageCheck size={18} /> Tác vụ đã sẵn sàng để thực hiện</div>}
    </div>
  );
}

export default App;