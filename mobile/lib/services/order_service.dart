import 'dart:convert';

import 'package:http/http.dart' as http;

import 'auth_service.dart';

class OrderService {
  static const String baseUrl = 'http://127.0.0.1:5000';

  final AuthService _authService = AuthService();

  Future<List<dynamic>> getOrders() async {
    final token = await _authService.getToken();

    if (token == null) {
      throw Exception('Bạn chưa đăng nhập');
    }

    final response = await http.get(
      Uri.parse('$baseUrl/api/orders'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );

    final data = jsonDecode(response.body);

    if (response.statusCode == 200) {
      return List<dynamic>.from(data);
    }

    throw Exception(
      data['error'] ?? 'Không thể tải danh sách đơn hàng',
    );
  }
}