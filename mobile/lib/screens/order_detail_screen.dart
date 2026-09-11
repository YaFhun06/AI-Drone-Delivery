import 'package:flutter/material.dart';

class OrderDetailScreen extends StatelessWidget {
final Map<String, dynamic> order;

const OrderDetailScreen({
super.key,
required this.order,
});

String _formatValue(dynamic value) {
if (value == null || value.toString().isEmpty) {
return 'Chưa có';
}
return value.toString();
}

Color _getStatusColor(String status) {
switch (status) {
case 'DELIVERED':
return Colors.green;
case 'APPROVED':
return Colors.blue;
case 'FAILED':
return Colors.red;
case 'PENDING':
return Colors.orange;
default:
return Colors.grey;
}
}

@override
Widget build(BuildContext context) {
final status = order['status']?.toString() ?? 'UNKNOWN';

return Scaffold(
  appBar: AppBar(
    title: const Text(
      'Chi tiết đơn hàng',
      style: TextStyle(
        fontWeight: FontWeight.bold,
      ),
    ),
    backgroundColor: const Color(0xFF0085FC),
    foregroundColor: Colors.white,
  ),
  body: SingleChildScrollView(
    padding: const EdgeInsets.all(16),
    child: Column(
      children: [
        Card(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              children: [
                Icon(
                  Icons.inventory_2,
                  size: 60,
                  color: _getStatusColor(status),
                ),
                const SizedBox(height: 12),
                Text(
                  'Đơn hàng #${order['id']}',
                  style: const TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 8),
                Chip(
                  label: Text(status),
                  backgroundColor:
                      _getStatusColor(status).withOpacity(0.15),
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 16),
        _buildInfoCard(
          icon: Icons.person,
          title: 'Khách hàng',
          value: _formatValue(order['customer_name']),
        ),
        _buildInfoCard(
          icon: Icons.refresh,
          title: 'Số lần giao lại',
          value: '${order['retry_count'] ?? 0} lần',
        ),
        _buildInfoCard(
          icon: Icons.schedule,
          title: 'Thời gian giao dự kiến',
          value: _formatValue(order['scheduled_time']),
        ),
        _buildInfoCard(
          icon: Icons.location_on,
          title: 'Trạm',
          value: _formatValue(order['station_id']),
        ),
        _buildInfoCard(
          icon: Icons.error_outline,
          title: 'Lý do giao thất bại',
          value: _formatValue(order['failure_reason']),
        ),
        _buildInfoCard(
          icon: Icons.calendar_today,
          title: 'Ngày tạo',
          value: _formatValue(order['created_at']),
        ),
      ],
    ),
  ),
);

}

Widget _buildInfoCard({
required IconData icon,
required String title,
required String value,
}) {
return Card(
margin: const EdgeInsets.only(bottom: 12),
child: ListTile(
leading: Icon(
icon,
color: const Color(0xFF0085FC),
),
title: Text(title),
subtitle: Text(
value,
style: const TextStyle(
fontSize: 16,
fontWeight: FontWeight.w500,
),
),
),
);
}
}
