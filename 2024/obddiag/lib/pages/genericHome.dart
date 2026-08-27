

import 'dart:async';
import 'dart:ffi';
import 'dart:io';


import 'package:flutter/material.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';
import 'dart:convert';
import 'dart:typed_data';
import 'package:convert/convert.dart';

Map vinYearDecode = {
  "0": "2000",
  "1": "2001",
  "2": "2002",
  "3": "2003",
  "4": "2004",
  "5": "2005",
  "6": "2006",
  "7": "2007",
  "8": "2008",
  "9": "2009",
  "A": "2010",
  "B": "2011",
  "C": "2012",
  "D": "2013",
  "E": "2014",
  "F": "2015",
  "G": "2016",
  "H": "2017",
  "I": "2018",
  "J": "2019",
  "K": "2020",
  "L": "2021",
  "M": "2022", 
  "N": "2023",
  "O": "2024",
  "P": "2025",
  "Q": "2026",
  "R": "2027",
  "S": "2028",  
  "T": "2029",
  "U": "2030",
  "V": "2031", 
  "W": "2032",
  "X": "2033",
  "Y": "2034", 
  "Z": "2035",

};

String DecodeVin({required String vin, required Map vinmap, required int index}) {
  print(vin);
  print(index);
  String vinatindex = vin[index-1];
  print(vinatindex);
  if (vinmap.containsKey(vinatindex)) {
    return vinmap[vinatindex];
  } else {
  return "";
  }
}

var a = 1;
var data2 = "";
void onDataRecieved (Uint8List data) {

  print("data: $data");
  data2 =  utf8.decode(data);
  data2 = data2.substring(0, data2.length-1);
  

}
Map XHK = {
  "G": "XK 4WD",
  "H": "XK 2WD",
  "3": "XH LHD",
  "1": "XH RHD",
};

Map Engines = {
  "K": "3.8L V6 Gasoline",
  "N": "4.7L V8 Gasoline",
  "2": "5.7L V8 Hemi Gasoline",
  "M": "3.0L CRD Diesel"
};
class GenericHome extends StatefulWidget {
  BluetoothConnection connection;
  GenericHome({super.key, required this.connection});
  @override
  _GenericHomeState createState() => _GenericHomeState(connection: connection);
  
}
String voltage = "";
class _GenericHomeState extends State<GenericHome> {
  BluetoothConnection connection;
  _GenericHomeState({required this.connection});
  String Voltage = "0";


  Future _sendData(String data) async{
    print(ascii.encode(data));
    connection.output.add(Uint8List.fromList(utf8.encode(data + "\r\n")));
    await connection.output.allSent;
    }


  String _sendCommand({required String command}) {
    sleep(Duration(milliseconds:  250));
    _sendData(command).then((value) {

        print(command);
        while (data2 == "") {
          sleep(Duration(milliseconds: 250));

        }
        
        
        
    },);
    print(data2);
    return data2;  
  }
    
  bool VoltageRead = false;
  String year = "";
  String model = "";
  String limited = "";
  String engine = "";
  String vinNum = "";
  @override
  Widget build(BuildContext context) {
    if (VoltageRead != true) {
      VoltageRead = true;
      connection.input?.listen(onDataRecieved);
      var data = _sendCommand(command: "09 02");

          print(data);
          data = data.replaceAll(" ", "");
          print(data);
          print(hex.decode(data));
          print(utf8.decode(hex.decode(data)));
          var vin = utf8.decode(hex.decode(data));
          var vinyr = DecodeVin(vin: vin, vinmap: vinYearDecode, index: 10);
          if (int.parse(vinyr)> 2010 || int.parse(vinyr) < 2006) {
            Widget okButton = TextButton(
              child: Text("OK"),
              onPressed: () { exit(0); },
            );
            
            AlertDialog alert = AlertDialog(
              title: Text("Error"),
              content: Text("Car is not a jeep commander xk/xh"),
              actions: [
                okButton,
              ],
            );

            showDialog(context: context, builder: (BuildContext builder) {return alert;} );

          }




      };
      var value = _sendCommand(command: "AT RV"); 
        setState(() {
             
              Voltage = value;
            });
          
      
    

    return Scaffold(
      appBar: AppBar(leading: IconButton(
        icon: Icon(Icons.arrow_back), onPressed: () {
          Navigator.pop(context);
        },
      ),
      title:Text("Jeep Commander $model $year"),
      centerTitle: true,
      ),
      body: Column(children: [Text("VIN: $vinNum"), Text("Full Model: Jeep Commander $limited $year $model $engine"), Text("Battery: $Voltage V")], crossAxisAlignment: CrossAxisAlignment.start,),
    );
  }
}
