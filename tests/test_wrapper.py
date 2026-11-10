import sys
from pathlib import Path
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import control
class WrapperTests(unittest.TestCase):
 def test_usb_status_and_set_are_preserved(self):
  for req in [{'op':'status','transport':'usb'},{'op':'set','transport':'usb','feature':'preset','value':0}]:
   with patch.object(control.headset,'dispatch',return_value={'ok':True}) as fn, patch.object(control.headset,'usb_link',return_value={'adapter':'present'}):
    self.assertEqual(control.dispatch(req),{'ok':True,'usb':{'adapter':'present'}});fn.assert_called_once_with(req)
 def test_link_is_usb_only_and_does_not_open_bluetooth(self):
  with patch.object(control.headset,'usb_link',return_value={'adapter':'missing'}) as usb, patch.object(control.headset,'dispatch') as fn:
   self.assertEqual(control.dispatch({'op':'link'}),{'ok':True,'usb':{'adapter':'missing'}})
   usb.assert_called_once_with();fn.assert_not_called()
 def test_invalid_transport_is_rejected(self):
  for transport in ('raw',None,''):
   with self.assertRaises(control.headset.HeadsetError):control.dispatch({'op':'status','transport':transport})
 def test_usb_gaming_is_rejected(self):
  with self.assertRaisesRegex(control.headset.HeadsetError,'bluetooth-only'):
   control.dispatch({'op':'set','transport':'usb','feature':'gaming','value':True})
 def test_no_firmware_or_pairing(self):
  for feature in ['firmware','pair','reset','poweroff','raw','sidetone']:
   with self.assertRaises(control.headset.HeadsetError):control.dispatch({'op':'set','transport':'bluetooth','feature':feature,'value':0})
 def test_native_request_is_preserved(self):
  req={'op':'set','transport':'bluetooth','address':'02:00:00:00:00:03','feature':'bands','value':[0]*10}
  with patch.object(control.headset,'dispatch',return_value={'ok':True}) as fn:
   self.assertEqual(control.dispatch(req),{'ok':True});fn.assert_called_once_with(req)
