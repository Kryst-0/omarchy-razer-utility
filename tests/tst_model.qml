import QtQuick
import QtTest
import "../DeviceModel.js" as Model
TestCase {
 name:"RazerBluetoothOnly"
 property string output:""
 property var devices:[{name:"Razer Barracuda X (BT)",address:"02:00:00:00:00:03",connected:true}]
 readonly property var selected:Model.bluetoothDevice(devices,output)
 function test_default_output_switch() {
  output="bluez_output.02_00_00_00_00_03.1";compare(selected.address,"02:00:00:00:00:03")
  output="bluez_output.02_00_00_00_00_01.1";compare(selected,null)
  output="alsa_output.usb-Razer_Barracuda_X_2.4";compare(selected,null)
 }
 function test_disconnected() {compare(Model.bluetoothDevice([{name:"Razer Barracuda X (BT)",address:"02:00:00:00:00:03",connected:false}],"bluez_output.02_00_00_00_00_03.1"),null)}
 function test_chroma_excluded() {verify(!Model.isBarracuda("Razer Barracuda X Chroma"))}
 function test_invalid_eq_not_exposed() {compare(Model.validState({preset:3,bands:[99],gaming:1,standby:-1}),({}))}
 function test_native_eq_bounds() {var s=Model.validState({preset:255,bands:[-5,-4,-3,-2,-1,0,1,2,4,5],gaming:false,standby:15});compare(s.preset,255);compare(s.bands.length,10);compare(s.gaming,false)}
 function test_markup_name_is_data() {var label='<img src="https://example.invalid/x">';var s=Model.validState({devices:[{address:"aabbccddeeff",active:false,name:label}]});compare(s.devices[0].name,label)}
 function test_bad_quick_connect_is_dropped() {compare(Model.validState({devices:[{address:"shell;command",active:false,name:"test"}]}).devices.length,0)}
}
