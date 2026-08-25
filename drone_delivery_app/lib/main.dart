import 'package:flutter/material.dart';
import 'screens/login_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SmartDrone Delivery',
      debugShowCheckedModeBanner: false, // Tắt chữ DEBUG màu đỏ
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF0085FC)),
        useMaterial3: true,
      ),
      home: const LoginScreen(),
    );
  }
}