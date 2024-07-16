// loading_screen.dart
import 'dart:math';
import 'package:artistry/screens/art/widgets/animated_loading_text.dart';
import 'package:flutter/material.dart';

class LoadingScreen extends StatelessWidget {
  LoadingScreen({super.key});

  final List<String> placeholderImages = [
    'assets/images/emoji/emoji1.png',
    'assets/images/emoji/emoji2.png',
    'assets/images/emoji/emoji3.png',
    'assets/images/emoji/emoji4.png',
    'assets/images/emoji/emoji5.png',
    'assets/images/emoji/emoji6.png',
    'assets/images/emoji/emoji7.png',
    'assets/images/emoji/emoji8.png',
    'assets/images/emoji/emoji9.png',
    'assets/images/emoji/emoji10.png',
  ];

  @override
  Widget build(BuildContext context) {
    final randomImage =
        placeholderImages[Random().nextInt(placeholderImages.length)];
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.asset(
              randomImage,
              width: 100,
            ),
            const SizedBox(height: 20),
            const AnimatedLoadingText(
              text: '잠시만 기다려주세요',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
