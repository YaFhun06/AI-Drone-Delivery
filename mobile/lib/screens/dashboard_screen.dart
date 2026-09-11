import 'package:flutter/material.dart';

import '../services/dashboard_service.dart';
import 'account_screen.dart';
import 'order_screen.dart';

class DashboardScreen extends StatefulWidget {
const DashboardScreen({super.key});

@override
State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
final DashboardService _dashboardService = DashboardService();

bool _isLoading = true;
String? _error;

int _deliveringDrones = 0;
int _deliveredOrders = 0;
int _approvedOrders = 0;
int _failedOrders = 0;

int _selectedIndex = 0;

@override
void initState() {
super.initState();
_loadDashboard();
}

Future<void> _loadDashboard() async {
try {
setState(() {
_isLoading = true;
_error = null;
});

  final data = await _dashboardService.getDashboardData();

  if (!mounted) return;

  setState(() {
    _deliveringDrones = data['deliveringDrones'] ?? 0;
    _deliveredOrders = data['deliveredOrders'] ?? 0;
    _approvedOrders = data['approvedOrders'] ?? 0;
    _failedOrders = data['failedOrders'] ?? 0;
    _isLoading = false;
  });
} catch (e) {
  if (!mounted) return;

  setState(() {
    _error = e.toString();
    _isLoading = false;
  });
}

}

void _onItemTapped(int index) {
if (index == 0) {
setState(() {
_selectedIndex = 0;
});
} else if (index == 1) {
Navigator.push(
context,
MaterialPageRoute(
builder: (context) => const OrderScreen(),
),
);
} else if (index == 2) {
Navigator.push(
context,
MaterialPageRoute(
builder: (context) => const AccountScreen(),
),
);
}
}

@override
Widget build(BuildContext context) {
return Scaffold(
appBar: AppBar(
title: const Text(
'Tổng Quan Trạm',
style: TextStyle(
fontWeight: FontWeight.bold,
color: Colors.white,
),
),
backgroundColor: const Color(0xFF0085FC),
elevation: 0,
actions: [
IconButton(
onPressed: _loadDashboard,
icon: const Icon(
Icons.refresh,
color: Colors.white,
),
),
],
),
body: _buildBody(),
bottomNavigationBar: BottomNavigationBar(
currentIndex: _selectedIndex,
onTap: _onItemTapped,
selectedItemColor: const Color(0xFF0085FC),
unselectedItemColor: Colors.grey,
items: const [
BottomNavigationBarItem(
icon: Icon(Icons.dashboard),
label: 'Tổng quan',
),
BottomNavigationBarItem(
icon: Icon(Icons.list_alt),
label: 'Đơn hàng',
),
BottomNavigationBarItem(
icon: Icon(Icons.person),
label: 'Tài khoản',
),
],
),
);
}

Widget _buildBody() {
if (_isLoading) {
return const Center(
child: CircularProgressIndicator(),
);
}

if (_error != null) {
  return Center(
    child: Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(
            Icons.error_outline,
            size: 60,
            color: Colors.red,
          ),
          const SizedBox(height: 16),
          const Text(
            'Không thể tải dữ liệu',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            _error!,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: _loadDashboard,
            child: const Text('Thử lại'),
          ),
        ],
      ),
    ),
  );
}

return RefreshIndicator(
  onRefresh: _loadDashboard,
  child: Padding(
    padding: const EdgeInsets.all(16),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Thống kê hôm nay',
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 16),
        Expanded(
          child: GridView.count(
            crossAxisCount: 2,
            crossAxisSpacing: 16,
            mainAxisSpacing: 16,
            childAspectRatio: 1.1,
            children: [
              _buildStatCard(
                'Drone đang giao',
                _deliveringDrones.toString(),
                const Color(0xFF0085FC),
                Icons.flight,
              ),
              _buildStatCard(
                'Đơn đã giao',
                _deliveredOrders.toString(),
                const Color(0xFF33A64C),
                Icons.check_circle,
              ),
              _buildStatCard(
                'Đơn chờ duyệt',
                _approvedOrders.toString(),
                const Color(0xFFCC6600),
                Icons.pending_actions,
              ),
              _buildStatCard(
                'Sự cố / lỗi',
                _failedOrders.toString(),
                const Color(0xFFDB2843),
                Icons.error,
              ),
            ],
          ),
        ),
      ],
    ),
  ),
);

}

Widget _buildStatCard(
String title,
String value,
Color color,
IconData icon,
) {
return Container(
decoration: BoxDecoration(
color: color.withOpacity(0.1),
borderRadius: BorderRadius.circular(16),
border: Border.all(
color: color.withOpacity(0.5),
width: 1.5,
),
),
child: Column(
mainAxisAlignment: MainAxisAlignment.center,
children: [
Icon(
icon,
size: 40,
color: color,
),
const SizedBox(height: 12),
Text(
value,
style: TextStyle(
fontSize: 28,
fontWeight: FontWeight.bold,
color: color,
),
),
const SizedBox(height: 4),
Text(
title,
textAlign: TextAlign.center,
style: const TextStyle(
fontSize: 14,
fontWeight: FontWeight.w600,
color: Colors.black87,
),
),
],
),
);
}
}
