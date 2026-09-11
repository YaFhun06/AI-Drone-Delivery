import 'dart:convert';
import 'package:http/http.dart' as http;

class DashboardService {
  static const String baseUrl = 'http://127.0.0.1:5000';

  Future<Map<String, int>> getDashboardData() async {
    try {
      final droneResponse = await http.get(
        Uri.parse('$baseUrl/api/drones'),
      );

      final orderResponse = await http.get(
        Uri.parse('$baseUrl/api/analytics/orders-by-status'),
      );

      int deliveringDrones = 0;
      int deliveredOrders = 0;
      int approvedOrders = 0;
      int failedOrders = 0;

      // Xử lý dữ liệu Drone
      if (droneResponse.statusCode == 200) {
        final List<dynamic> drones =
            jsonDecode(droneResponse.body);

        deliveringDrones = drones.where((drone) {
          return drone['status'] == 'DELIVERING';
        }).length;
      }

      // Xử lý dữ liệu Order
      if (orderResponse.statusCode == 200) {
        final Map<String, dynamic> orderData =
            jsonDecode(orderResponse.body);

        final Map<String, dynamic> byStatus =
            Map<String, dynamic>.from(
          orderData['by_status'] ?? {},
        );

        deliveredOrders =
            (byStatus['DELIVERED'] ?? 0) as int;

        approvedOrders =
            (byStatus['APPROVED'] ?? 0) as int;

        failedOrders =
            (byStatus['FAILED'] ?? 0) as int;
      }

      return {
        'deliveringDrones': deliveringDrones,
        'deliveredOrders': deliveredOrders,
        'approvedOrders': approvedOrders,
        'failedOrders': failedOrders,
      };
    } catch (e) {
      throw Exception('Không thể tải dữ liệu Dashboard: $e');
    }
  }
}