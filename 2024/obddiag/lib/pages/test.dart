
import 'package:flutter/material.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';
import 'package:obddiag/pages/genericHome.dart';

class BluetoothSetupPage extends StatefulWidget {
  @override
  _BluetoothSetupPageState createState() => _BluetoothSetupPageState();
}

class _BluetoothSetupPageState extends State<BluetoothSetupPage> {
  late BluetoothConnection _connection;

  @override
  void initState() {
    super.initState();
    _connectToDeviceByName();
  }

  Future<void> _connectToDeviceByName() async {
    List<BluetoothDevice> devices = await FlutterBluetoothSerial.instance.getBondedDevices();
    String desiredDeviceName = 'OBDII'; // Replace with the actual device name
    BluetoothDevice? device;
    try {
      device = devices.firstWhere((d) => d.name == desiredDeviceName);
    } catch(error) {
      print(error);
      device = null;
    }

    if (device != null) {
      try {
        _connection = await BluetoothConnection.toAddress(device.address);
        print('Connected to ${device.name}');
        setState(() {
          BluetoothText = "Connected to OBD II Reader";
        });
        Navigator.push(context, MaterialPageRoute(builder: (context) => GenericHome(connection: _connection)));

      } catch (error) {
        print('Error connecting to device: $error');
        setState(() {
          BluetoothText = "Error, could not connect";
        });
      }
    } else {
      print('Device not found: $desiredDeviceName');
      setState(() {
        BluetoothText = "no device found";
      });
    }
  }
  String BluetoothText = "Connecting....";
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Bluetooth Setup'),
      ),
      body: Center(
        child: Text(BluetoothText),
      ),
    );
  }
}