# Razer Utility

Separate Omarchy bar widget for Razer Barracuda X (2022), Bluetooth only.
Follows the default PipeWire output and hides when a connected supported
Barracuda Bluetooth endpoint is not the default. No device selector or USB support.

The panel uses the same Omarchy components, battery meter, theme, rotating phrases
and icon style as JBL Utility. Click opens it; middle click mutes the current
Barracuda output, scrolling adjusts system output volume.

Headset settings are real native commands over the paired headset's Bluetooth
Classic serial service, with dynamically discovered RFCOMM channel:
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

Only an explicit panel open or refresh reads the settings. There is no scan,
pairing, reset, firmware operation, background monitor or automatic reconnect.
Finite helper requests are limited to 35 seconds. Bluetooth battery is read from
Quickshell/BlueZ. The custom EQ levels are relative units, not calibrated dB.

Native transport and protocol helpers are vendored from
https://github.com/leag/razer-barracuda (MIT, license in vendor/LICENSE).
Upstream revision is recorded in vendor/UPSTREAM.txt. USB functions retained in
that library are not reachable through this plugin's Bluetooth-only allowlist.

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

## Remove

```sh
omarchy plugin remove krysto.razer-utility
```
