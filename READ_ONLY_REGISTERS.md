# Read-only HP register coverage

The EATM00 (ecoGEO HP) map contains 360 named readings: the 263 entries in
Ecoforest's Modbus 2023 v02 HP tables (pp. 11–17), plus 97 settings/status fields
mapped by the installed EGW_v2.18 `gama2` web client. Domestic models retain
their separate existing map. Do not apply domestic addresses or blanket offsets
to the HP controller.

`modbus_info.json` and `registers.py` are identical in this repository and its
companion (ostracon/ecoforest-ecogeo-api / ostracon/ecoforest_ecogeo). Maintain
both copies together. Each HP field specifies its key, bank, address, scale,
unit type, source and any limitations. Existing entity keys are preserved.
Integer web-array index n maps to HTTP register n+5001; analog and boolean
indices are used directly. Check the field's source before adding an address.

## Read-only enforcement

The HTTP transport accepts only operations 2001 (coil read) and 2002 (register
read), with exactly the address/count arguments. Every other operation or
payload is rejected before network I/O, including inherited control methods.
No number, switch, button or climate platform is loaded by Home Assistant.
`rw` in the source map describes the manufacturer's register capability; it
never grants the client permission to write.

Reads are sequential, confined to mapped addresses, grouped into blocks of at
most 64 and separated by 50 ms. HA retains its 60-second polling interval.
New fields are optional: a rejected block becomes unavailable rather than
zero or stale data; core telemetry continues. Required HA reads retry up to
three times; exhausted retries make the coordinator unavailable. Authentication
failures always propagate. Responses must match the requested operation,
address, count and payload format. Signed decoding includes 0x8000; absent
probes (-999.9°C) become unavailable. Coils are exposed as numeric 0/1 sensors.

## Interpretation and limits

- Heating adjustment 5072–5076 is an enum: 0..4 means -4,-2,0,+2,+4°C.
  It is separate from DT start (117), DT heating (141), and DT supply (65).
- Demand slots 5139–5142 decode the web client's demand list. They are not
  valve-position feedback or proof of uninterrupted service changeover.
- Mode inputs 5085–5088 are raw inputs used jointly by the web status icons;
  they are not exclusive active-service enums.
- Priority selections 5039–5043 and delay 5173 remain explicitly unvalidated.
  A zero does not establish equal priorities or disabled protection. No
  minutes-per-hour setting has been verified for this controller.
- Existing energy-counter units and annual PF scaling are not reinterpreted.
  The new energy-unit flags expose evidence for a separate validation; do not
  use unvalidated counters for billing. The map preserves existing IDs.
- HA attributes include source, register address/bank, raw value and notes.
  Optional fields accepted by the gateway can still be unused on a particular
  firmware/model. Availability alone does not prove their meaning.

This update does not change compressor protection, priorities, temperatures,
service selection or any heat-pump settings. It supplies diagnostic evidence;
it does not assert a cause or remedy for pool-to-buffer compressor stops.

## Offline validation

Run the unittest suite with httpx and (for the HA API tests) pyecoforest 0.4.0.
Tests use a mock HTTP transport; HA API tests isolate runtime imports and do
not pretend to validate the HA frontend. They cover transport write rejection,
response validation, sign/scaling, request coverage, optional failures,
authentication and required retry exhaustion. Live testing is separate.
