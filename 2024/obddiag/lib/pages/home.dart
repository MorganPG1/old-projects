import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:obddiag/pages/genericHome.dart';
import 'package:obddiag/pages/test.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      
      appBar: AppBar(
        title: Text("Jeep Commander Toolkit"),
        centerTitle: true,
        backgroundColor: Color.fromARGB(255, 255, 96, 96),
        elevation: 15,
        bottomOpacity: 0,
      ),

      body: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const Padding(padding: EdgeInsets.all(8)),
              TextButton(
                onPressed:() {
                  Navigator.push(context, MaterialPageRoute(builder: (context) => new BluetoothSetupPage()));
                },style: const ButtonStyle(backgroundColor: WidgetStatePropertyAll(Colors.red)) ,
                child: const Text("Jeep Commander XH/K ", style: TextStyle(color: Colors.black ), )
              ),


            ],
            )
        ],
      ),
    );
  }
}