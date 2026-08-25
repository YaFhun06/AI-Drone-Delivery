import 'package:flutter/material.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Logo minh họa
              const Icon(
                Icons.flight_takeoff,
                size: 80,
                color: Color(0xFF0085FC), // Màu Primary Blue Tech
              ),
              const SizedBox(height: 32),
              
              // Tiêu đề app
              const Text(
                'SmartDrone Delivery',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: Colors.black87,
                ),
              ),
              const SizedBox(height: 48),

              // Ô nhập Email
              TextField(
                decoration: InputDecoration(
                  labelText: 'Email / Tên đăng nhập',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  prefixIcon: const Icon(Icons.person),
                ),
              ),
              const SizedBox(height: 16),

              // Ô nhập Mật khẩu
              TextField(
                obscureText: true,
                decoration: InputDecoration(
                  labelText: 'Mật khẩu',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  prefixIcon: const Icon(Icons.lock),
                ),
              ),
              const SizedBox(height: 32),

              // Nút Đăng nhập
              ElevatedButton(
                onPressed: () {
                  // TODO: Xử lý chuyển trang sau khi đăng nhập
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF0085FC), // Màu Blue Tech
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30), // Nút Pill/Rounded
                  ),
                ),
                child: const Text(
                  'ĐĂNG NHẬP',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}