function isBarracuda(text) {
  return /razer[\s_\-]*barracuda[\s_\-]*x(?:[\s_\-]|\(|$)/i.test(String(text || ""))
      && !/chroma|2021/i.test(String(text || ""))
}
function bluetoothDevice(devices, output) {
  var name = String(output || "").toLowerCase()
  for (var i = 0; i < devices.length; i++) {
    var d = devices[i]
    if (!d || !d.connected || !isBarracuda(d.name || d.deviceName)) continue
    var addr = String(d.address || "").replace(/:/g, "_").toLowerCase()
    if (addr && name.indexOf(addr) >= 0) return d
  }
  return null
}
function validState(state) {
  if (!state || typeof state !== "object") return ({})
  var out = {}
  if ([0,7,8,9,255].indexOf(state.preset) >= 0) out.preset = state.preset
  if ([0,5,15,30,45,60].indexOf(state.standby) >= 0) out.standby = state.standby
  if (typeof state.gaming === "boolean") out.gaming = state.gaming
  if (typeof state.dnd === "boolean") out.dnd = state.dnd
  if (Array.isArray(state.bands) && state.bands.length === 10 && state.bands.every(v => Number.isInteger(v) && v >= -5 && v <= 5)) out.bands = state.bands
  if (Array.isArray(state.devices)) out.devices = state.devices.slice(0,16).filter(d => d && /^[0-9a-f]{12}$/i.test(d.address) && typeof d.active === "boolean" && typeof d.name === "string" && d.name.length <= 128)
  return out
}
