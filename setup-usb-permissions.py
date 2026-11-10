#!/usr/bin/python3
"""Grant a user's primary group access to this dongle's settings mailbox only."""
import os
from pathlib import Path
import pwd
import subprocess
import sys


def main():
    if os.geteuid() != 0 or len(sys.argv) != 2:
        raise SystemExit('Run as root with the desktop username as the only argument.')
    user = pwd.getpwnam(sys.argv[1])
    if user.pw_uid < 1000:
        raise SystemExit('A regular desktop user is required.')
    rule = ('ACTION=="bind", SUBSYSTEM=="hid", DRIVER=="razer-barracuda", '
            'ENV{HID_ID}=="0003:00001532:00000552", TEST=="headset_settings", '
            f'RUN+="/usr/bin/chgrp {user.pw_gid} /sys%p/headset_settings", '
            'RUN+="/usr/bin/chmod 0660 /sys%p/headset_settings"\n')
    target = Path('/etc/udev/rules.d/99-razer-utility-settings.rules')
    if target.is_symlink():
        raise SystemExit('Refusing symlink destination.')
    target.write_text('# Razer Utility: access to the serialized settings mailbox.\n' + rule)
    target.chmod(0o644)
    subprocess.run(['udevadm', 'control', '--reload-rules'], check=True)
    for device in Path('/sys/bus/hid/devices').glob('0003:1532:0552.*'):
        if (device / 'driver').resolve().name != 'razer-barracuda':
            continue
        if (device.resolve().parent / 'bInterfaceNumber').read_text().strip() != '03':
            continue
        mailbox = device / 'headset_settings'
        if mailbox.exists():
            os.chown(mailbox, 0, user.pw_gid)
            mailbox.chmod(0o660)
    print('USB settings access installed; no logout required.')


if __name__ == '__main__':
    main()
