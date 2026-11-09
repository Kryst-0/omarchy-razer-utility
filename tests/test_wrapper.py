import sys
from pathlib import Path
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import control
class WrapperTests(unittest.TestCase):
 def test_usb_and_link_are_rejected(self):
  for req in [{'op':'link'},{'op':'status','transport':'usb'},{'op':'set','transport':'usb','feature':'preset','value':0}]:
   with self.assertRaises(control.headset.HeadsetError):control.dispatch(req)
 def test_no_firmware_or_pairing(self):
  for feature in ['firmware','pair','reset','poweroff','raw','sidetone']:
   with self.assertRaises(control.headset.HeadsetError):control.dispatch({'op':'set','transport':'bluetooth','feature':feature,'value':0})
 def test_native_request_is_preserved(self):
  req={'op':'set','transport':'bluetooth','address':'02:00:00:00:00:03','feature':'bands','value':[0]*10}
  with patch.object(control.headset,'dispatch',return_value={'ok':True}) as fn:
   self.assertEqual(control.dispatch(req),{'ok':True});fn.assert_called_once_with(req)
