import 'package:flutter/material.dart';

import '../services/order_service.dart';
import 'order_detail_screen.dart';

class OrderScreen extends StatefulWidget {
const OrderScreen({super.key});

@override
State<OrderScreen> createState() => _OrderScreenState();
}

class _OrderScreenState extends State<OrderScreen> {
final OrderService _orderService = OrderService();

bool _isLoading = true;
String? _error;
List<dynamic> _orders = [];

@override
void initState() {
super.initState();
_loadOrders();
}

Future<void> _loadOrders() async {
setState(() {
_isLoading = true;
_error = null;
});

try {
  final orders = await _orderService.getOrders();

  if (!mounted) return;

  setState(() {
    _orders = orders;
    _isLoading = false;
  });
} catch (e) {
  if (!mounted) return;

  setState(() {
    _error = e.toString().replaceFirst('Exception: ', '');
    _isLoading = false;
  });
}

}

Color _getStatusColor(String status) {
switch (status) {
case 'DELIVERED':
return const Color(0xFF2EAD5B);
case 'APPROVED':
return const Color(0xFF0085FC);
case 'FAILED':
return const Color(0xFFDB2843);
case 'PENDING':
return const Color(0xFFFF9800);
default:
return Colors.grey;
}
}

IconData _getStatusIcon(String status) {
switch (status) {
case 'DELIVERED':
return Icons.check_circle;
case 'APPROVED':
return Icons.pending_actions;
case 'FAILED':
return Icons.error;
case 'PENDING':
return Icons.schedule;
default:
return Icons.inventory_2;
}
}

String _getStatusText(String status) {
switch (status) {
case 'DELIVERED':
return 'Đã giao';
case 'APPROVED':
return 'Đã duyệt';
case 'FAILED':
return 'Thất bại';
case 'PENDING':
return 'Chờ xử lý';
default:
return status;
}
}

@override
Widget build(BuildContext context) {
return Scaffold(
backgroundColor: const Color(0xFFF5F7FA),
appBar: AppBar(
title: const Text(
'Danh sách đơn hàng',
style: TextStyle(
fontWeight: FontWeight.bold,
),
),
backgroundColor: const Color(0xFF0085FC),
foregroundColor: Colors.white,
elevation: 0,
actions: [
IconButton(
onPressed: _loadOrders,
icon: const Icon(Icons.refresh),
),
],
),
body: RefreshIndicator(
onRefresh: _loadOrders,
child: _buildBody(),
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
  return ListView(
    children: [
      SizedBox(
        height: 500,
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(
                  Icons.error_outline,
                  size: 70,
                  color: Colors.red,
                ),
                const SizedBox(height: 16),
                const Text(
                  'Không thể tải đơn hàng',
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
                const SizedBox(height: 20),
                ElevatedButton.icon(
                  onPressed: _loadOrders,
                  icon: const Icon(Icons.refresh),
                  label: const Text('Thử lại'),
                ),
              ],
            ),
          ),
        ),
      ),
    ],
  );
}

if (_orders.isEmpty) {
  return ListView(
    children: const [
      SizedBox(
        height: 500,
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.inventory_2_outlined,
                size: 70,
                color: Colors.grey,
              ),
              SizedBox(height: 16),
              Text(
                'Chưa có đơn hàng',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ),
      ),
    ],
  );
}

return ListView.builder(
  padding: const EdgeInsets.all(16),
  itemCount: _orders.length,
  itemBuilder: (context, index) {
    final order = _orders[index];
    final status = order['status']?.toString() ?? 'UNKNOWN';
    final color = _getStatusColor(status);
    final retryCount = order['retry_count'] ?? 0;

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      child: Material(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        elevation: 2,
        shadowColor: Colors.black12,
        child: InkWell(
          borderRadius: BorderRadius.circular(18),
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => OrderDetailScreen(
                  order: Map<String, dynamic>.from(order),
                ),
              ),
            );
          },
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Container(
                  width: 55,
                  height: 55,
                  decoration: BoxDecoration(
                    color: color.withOpacity(0.12),
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Icon(
                    _getStatusIcon(status),
                    color: color,
                    size: 30,
                  ),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Đơn hàng #${order['id']}',
                        style: const TextStyle(
                          fontSize: 17,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 6),
                      Text(
                        'Khách hàng: ${order['customer_name'] ?? 'N/A'}',
                        style: const TextStyle(
                          color: Colors.black54,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 10,
                              vertical: 5,
                            ),
                            decoration: BoxDecoration(
                              color: color.withOpacity(0.12),
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: Text(
                              _getStatusText(status),
                              style: TextStyle(
                                color: color,
                                fontSize: 12,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                          if (retryCount > 0) ...[
                            const SizedBox(width: 8),
                            Text(
                              'Giao lại: $retryCount lần',
                              style: const TextStyle(
                                fontSize: 12,
                                color: Colors.black45,
                              ),
                            ),
                          ],
                        ],
                      ),
                    ],
                  ),
                ),
                const Icon(
                  Icons.arrow_forward_ios,
                  size: 18,
                  color: Colors.grey,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  },
);

}
}
