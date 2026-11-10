#!/usr/bin/python3
"""Finite native Barracuda X 2022 requests. No software DSP or firmware operations."""
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'vendor'))
from barracuda_pair import headset

def dispatch(request):
    if not isinstance(request,dict) or request.get('op') not in ('link','status','set'):
        raise headset.HeadsetError('invalid-request')
    if request.get('op') == 'link':
        return {'ok': True, 'usb': headset.usb_link()}
    if request.get('transport') not in ('bluetooth', 'usb'):
        raise headset.HeadsetError('invalid-request')
    if request.get('op') == 'set':
        if request.get('feature') not in headset.FEATURES:
            raise headset.HeadsetError('invalid-request')
        if request.get('feature') == 'gaming' and request.get('transport') != 'bluetooth':
            raise headset.HeadsetError('bluetooth-only')
    result = headset.dispatch(request)
    if request.get('transport') == 'usb':
        result['usb'] = headset.usb_link()
    return result

if __name__=='__main__':
    try:
        if len(sys.argv)!=2 or len(sys.argv[1])>2048: raise ValueError('Invalid request')
        result=dispatch(json.loads(sys.argv[1]))
    except (headset.HeadsetError,OSError) as exc:
        result={'ok':False,'error':headset.error_code(exc)}
    except (ValueError,TypeError,KeyError): result={'ok':False,'error':'invalid-request'}
    print(json.dumps(result,ensure_ascii=False))
