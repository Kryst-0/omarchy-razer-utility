# Razer Utility

Separate Omarchy bar widget for Razer Barracuda X (2022), over Bluetooth or the
USB 2.4 GHz dongle (`1532:0552`). Follows the default PipeWire output and hides
when a supported Barracuda endpoint is not the default. No device selector.

The panel uses the same Omarchy components, battery meter, theme, rotating phrases
and icon style as JBL Utility. Click opens it; middle click mutes the current
Barracuda output, scrolling adjusts system output volume.

Headset settings are real native commands over the paired headset's Bluetooth
Classic serial service (dynamically discovered RFCOMM channel), or the USB
driver's serialized settings mailbox:
- Internal EQ: Default, Game, Music, Movie, Custom.
- Ten custom bands: 31 Hz through 16 kHz, relative levels -5 through +5.
- Bluetooth gaming mode and Do Not Disturb.
- Idle shutdown: never, 5, 15, 30, 45 or 60 minutes.
- Known Bluetooth sources / Quick Connect. An accepted request is not a confirmed
  source change. Gaming must be off before switching hosts.

EQ is stored in the headset. No PipeWire filter, EasyEffects, microphone DSP,
virtual audio device or software EQ is created. A feature appears only after a
valid native GET. Each setting write is followed by a GET; rejected or unconfirmed
values are cleared. EQ bands are sent together, debounced after release.

Only an explicit panel open or refresh reads the settings. USB link and battery
are read from the driver's cached sysfs values every five seconds while its
output is selected; these reads send no hardware requests. USB presence alone
does not confirm a headset connection. There is no scan,
pairing, reset, firmware operation, background monitor or automatic reconnect.
Finite helper requests are limited to 35 seconds. Bluetooth battery is read from
Quickshell/BlueZ. The custom EQ levels are relative units, not calibrated dB.

Native transport and protocol helpers are vendored from
https://github.com/leag/razer-barracuda (MIT, license in vendor/LICENSE).
Upstream revision is recorded in vendor/UPSTREAM.txt. USB controls use the same
native request validation and readback as Bluetooth. Gaming remains Bluetooth-only;
USB does not establish activation.

USB requires the upstream `hid-razer-barracuda` DKMS driver (0.6.0 or later),
matching kernel headers and write access to its `headset_settings` attribute.
See https://github.com/leag/razer-barracuda/blob/main/docs/DKMS.md . The plugin
does not replace the USB audio driver or install the optional ALSA jack quirk.
The driver serializes explicit requests with its native battery queries.

Physical validation: a connected Barracuda X (BT) answered all six feature GETs;
preset 0 was written back unchanged and confirmed with GET. Initial settings
were preserved. Gaming latency and switching to other hosts were not physically
tested. Synthetic transport tests cover replies, SDP discovery, native write
readback, rejects and malformed data; QML tests cover default-output changes and
feature validation.

Tests:
PYTHONPATH=vendor python3 -m unittest discover -s tests -v
QT_QPA_PLATFORM=offscreen QT_QPA_PLATFORMTHEME= QT_QUICK_CONTROLS_STYLE=Basic /usr/lib/qt6/bin/qmltestrunner -input tests/tst_model.qml
omarchy plugin validate .

## Install

```sh
omarchy plugin add https://github.com/Kryst-0/omarchy-razer-utility.git --enable
```

For USB, install the upstream DKMS driver first. If your desktop user does not
belong to `audio`, grant its primary group access to the settings mailbox:

```sh
pkexec python3 ~/.config/omarchy/plugins/krysto.razer-utility/setup-usb-permissions.py "$USER"
```

This installs a device-specific udev rule and updates only the settings mailbox
of the matching bound dongle. It does not grant raw USB access or power-off access.

## Remove

```sh
omarchy plugin remove krysto.razer-utility
```
