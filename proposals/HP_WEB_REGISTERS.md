# HP web-register expansion ledger

**Promoted: 115 high-confidence additions; 91 deferred references.**
All 206 additional literal references from 25 installed EGW_v2.18 `gama2`
scripts are accounted for in [hp-web-registers.json](hp-web-registers.json).
Both packages now include the 115 reviewed definitions, taking the production
map from 360 to 475 readings. No existing key, normalized name or bank/address
pair was reused. No heat-pump setting was changed.

## Findings useful for heating diagnosis

- Automatic winter/summer selection is independent of the fixed heating curve:
  analog 121/122 are summer/winter thresholds, integer 5063 is programme,
  5064 is the seasonal change delay **in hours**, and coil 206 is current season.
  These can help explain seasonal eligibility; they do not explain the observed
  pool-to-buffer stop by themselves.
- Night mode has enable coil 132, start/end hour/minute 5065–5068, and compressor
  capacity limit 5069 (%). The HTML positions and bounds establish the time
  components: the misleading `min_fin` ID at **5067 is the end hour**.
  The domestic `gama1` pool script uses that address for minutes/hour; this HP
  script does not. Shared translation text is not evidence of an HP feature.
- Analog 103–106 are **pump-capacity limits (%)**, despite element IDs containing
  `temp` and `pres`. Analog 107/108/143 are temperature protections, 109/110
  pressure protections. These are settings, not current output or protection
  countdowns.
- DHW user target 40 is distinct from information-page target 38. Preserve both
  addresses; propose clarifying 38's existing display label without changing its
  key. DHW DT 166 and legionella setpoint 94 are not heating-buffer limits.
- Coil 82 is labelled simultaneous **heating/cooling consumption**. It is not
  pool/buffer equal priority or a guarantee of uninterrupted service changeover.
- Priority extras 118/119/5052 remain deferred: 119 is a Save field, and no
  operational meaning was identified for 118/5052. No new minimum-start-interval,
  minimum-stop-time or seamless-changeover parameter was established.
- Compressor starts likely combine 5008*10000+5009; operating hours likely
  combine 5010*1000+5011. Those are inferences from string formatting, not
  validated counters. The starts/hour components produced an implausible
  negative value, and the JavaScript contains a padding/index bug. Defer derived
  totals/rates until controller-screen comparison and rollover/reset checks.

## Promoted fields

The manifest supplies names, stable proposed keys, bank/address, scale, optional
status, bounds/enums where supported, source hashes/read blocks, and limitations.
It covers seasonal and night settings; protection limits; DHW, auxiliary and
recirculation settings; cooling enable/adjustment; floor drying; clock-change
schedules; and E-manager status/power fields. Some are irrelevant when optional
hardware is not fitted. Configuration enable flags are not running feedback.

The 115 proposed fields returned valid, decodable responses in
32 sequential read requests on V07 B19. This confirms the
read path on one controller, not the physical meaning or universal support of
every optional feature. Private live values remain outside these repositories.

The proposal deliberately uses existing decoder types: numeric 0/1 coils,
integer enums only, signed/scaled analogs. Duration units are explicit in names
and notes pending a typed-duration entity change. Programme code 3 stays raw:
the captured English translation is missing, so no label is invented.

## Promotion and acceptance checks

1. The reviewed definitions are present in both HP maps, preserving all
   existing keys and the separate domestic map. HA names/translations were added
   with the promotion. Add duration units and consider conditional availability for
   inactive floor-drying/optional hardware before exposing those fields broadly.
2. Keep sensor-only platforms and the existing transport guard (only operations
   2001/2002, exact read payload). No setter, Save/reset operation, schedule write,
   protection change or web-page execution is needed.
3. Keep new fields optional. Test failure isolation on the combined map: promotion
   can join new fields to existing optional blocks, so a firmware-specific
   rejection could affect neighbouring optional readings. Split groups or slow
   settings polling if necessary after measuring performance.
4. The existing planner produces 66 blocks for 475 named
   addresses, versus 49 blocks before promotion. The standalone proposal check used
   32 blocks; it is not a benchmark of combined HA polling.
5. Seasonal mode/thresholds, night enable/limit and pump/protection settings are
   exposed for diagnosis. Recirculation, cooling, floor-drying and E-manager
   groups remain optional diagnostics. Do not infer service behaviour from them.
6. Compare the actual controller screen for the deferred entries. Obtain installer
   HTML/option labels through authorized access when possible; preserve unknown
   codes. For counters, observe increments/resets before adding total-increasing
   statistics. Do not enable hardware or trigger cycles merely to validate reads.

Do not execute the stock homepage to collect readings: its initialization can
automatically synchronize the controller clock. Fetch source as text and use the
guarded register-read client. Installer HTML remains protected even though its
JavaScript can be fetched; this proposal does not bypass that boundary.

## Complete candidate ledger

`A` = analog, `I` = integer, `B` = coil. Addresses are HTTP addresses, not manual
table offsets. Integer web index n maps to HTTP n+5001. Analog/coil indices map
directly. The JSON records the exact source script hashes and read blocks; the
captured vendor sources are retained in the local investigation, not bundled.

| Bank/address | Disposition | Meaning | Qualification |
| --- | --- | --- | --- |
| A37 | proposed | Floor drying current phase temperature | The web display suppresses this when phase register 5089 is zero. A readable value alone does not mean floor drying is active. |
| A40 | proposed | DHW user target | acs_usuario set_p_1, distinct from information-page target 38. Do not merge these or infer their difference without observing both. |
| A68 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A69 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A70 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A71 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A72 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A73 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A74 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A75 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A76 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A77 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A78 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A79 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A80 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A81 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A82 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A83 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A84 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A85 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A86 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A87 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A88 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A89 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A90 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A91 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A92 | deferred | Cooling curve/fixed-temperature parameters for groups 1..5 | Bindings three/one/two/four/five identify the group and graph role, but protected HTML is needed to verify each coordinate/endpoint. Do not guess axes from variable names. |
| A93 | proposed | Cooling DT supply | Setting readback; does not establish a restart interval, buffer overshoot or service-changeover rule. |
| A94 | proposed | DHW legionella setpoint | Setting readback; does not establish a restart interval, buffer overshoot or service-changeover rule. |
| A103 | proposed | Production pump minimum capacity | Protection page pump-capacity section; validation bounds 30..100. Misleading element IDs contain temp/pres; these are capacity limits, not temperatures or pressures. |
| A104 | proposed | Production pump maximum capacity | Protection page pump-capacity section; validation bounds 30..100. Misleading element IDs contain temp/pres; these are capacity limits, not temperatures or pressures. |
| A105 | proposed | Brine pump minimum capacity | Protection page pump-capacity section; validation bounds 30..100. Misleading element IDs contain temp/pres; these are capacity limits, not temperatures or pressures. |
| A106 | proposed | Brine pump maximum capacity | Protection page pump-capacity section; validation bounds 30..100. Misleading element IDs contain temp/pres; these are capacity limits, not temperatures or pressures. |
| A107 | proposed | Minimum brine temperature | Setting readback; does not establish a restart interval, buffer overshoot or service-changeover rule. |
| A108 | proposed | Minimum production temperature for cooling | Setting readback; does not establish a restart interval, buffer overshoot or service-changeover rule. |
| A109 | proposed | Minimum brine pressure | Protection setting readback, not measured pressure. |
| A110 | proposed | Minimum production pressure | Protection setting readback, not measured pressure. |
| A121 | proposed | Automatic summer threshold | Setting readback; does not establish a restart interval, buffer overshoot or service-changeover rule. |
| A122 | proposed | Automatic winter threshold | Setting readback; does not establish a restart interval, buffer overshoot or service-changeover rule. |
| A140 | proposed | Cooling DT cooling | Setting readback; does not establish a restart interval, buffer overshoot or service-changeover rule. |
| A143 | proposed | Maximum brine temperature | Setting readback; does not establish a restart interval, buffer overshoot or service-changeover rule. |
| A145 | proposed | Cooling DT dew point | Setting readback; does not establish a restart interval, buffer overshoot or service-changeover rule. |
| A146 | deferred | BUS room-terminal DT for groups 1..5 | gd_dt fields occur in both heating/cooling installer scripts. Relationship to DT S/W Off/On and interior compensation is not sufficiently resolved. |
| A147 | deferred | BUS room-terminal DT for groups 1..5 | gd_dt fields occur in both heating/cooling installer scripts. Relationship to DT S/W Off/On and interior compensation is not sufficiently resolved. |
| A148 | deferred | BUS room-terminal DT for groups 1..5 | gd_dt fields occur in both heating/cooling installer scripts. Relationship to DT S/W Off/On and interior compensation is not sufficiently resolved. |
| A149 | deferred | BUS room-terminal DT for groups 1..5 | gd_dt fields occur in both heating/cooling installer scripts. Relationship to DT S/W Off/On and interior compensation is not sufficiently resolved. |
| A150 | deferred | BUS room-terminal DT for groups 1..5 | gd_dt fields occur in both heating/cooling installer scripts. Relationship to DT S/W Off/On and interior compensation is not sufficiently resolved. |
| A166 | proposed | DHW DT DHW | Setting readback; does not establish a restart interval, buffer overshoot or service-changeover rule. |
| A221 | proposed | E-manager consumption limit setpoint | Principal/user HTML explicitly displays kW. Requires the grid meter/control feature; accepted reads do not prove it is fitted. Sign convention of control actual power remains unverified. |
| A222 | proposed | E-manager surplus balance setpoint | Principal/user HTML explicitly displays kW. Requires the grid meter/control feature; accepted reads do not prove it is fitted. Sign convention of control actual power remains unverified. |
| A223 | deferred | E-manager surplus activation/deactivation thresholds | Names are clear; installer HTML/unit and sign semantics not verified. Do not assume kW merely because adjacent fields use it. |
| A224 | deferred | E-manager surplus activation/deactivation thresholds | Names are clear; installer HTML/unit and sign semantics not verified. Do not assume kW merely because adjacent fields use it. |
| A225 | proposed | E-manager grid consumption power | Principal/user HTML explicitly displays kW. Requires the grid meter/control feature; accepted reads do not prove it is fitted. Sign convention of control actual power remains unverified. |
| A226 | proposed | E-manager grid injection power | Principal/user HTML explicitly displays kW. Requires the grid meter/control feature; accepted reads do not prove it is fitted. Sign convention of control actual power remains unverified. |
| A227 | proposed | E-manager grid control actual power | Principal/user HTML explicitly displays kW. Requires the grid meter/control feature; accepted reads do not prove it is fitted. Sign convention of control actual power remains unverified. |
| B49 | deferred | Heating group thermostat configuration/logic | gdNe_2 selector values lack verified option labels; not a demand flag. |
| B50 | deferred | Heating group thermostat configuration/logic | gdNe_2 selector values lack verified option labels; not a demand flag. |
| B51 | deferred | Heating group thermostat configuration/logic | gdNe_2 selector values lack verified option labels; not a demand flag. |
| B52 | deferred | Heating group thermostat configuration/logic | gdNe_2 selector values lack verified option labels; not a demand flag. |
| B53 | deferred | Heating group thermostat configuration/logic | gdNe_2 selector values lack verified option labels; not a demand flag. |
| B60 | proposed | DHW production pump configured | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B61 | proposed | DHW recirculation pump configured | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B66 | proposed | Active cooling production pump configured | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B67 | proposed | Cooling group 1 configured | Installer group enable selection; not a cooling demand or active-service flag. |
| B68 | proposed | Cooling group 2 configured | Installer group enable selection; not a cooling demand or active-service flag. |
| B69 | proposed | Cooling group 3 configured | Installer group enable selection; not a cooling demand or active-service flag. |
| B70 | proposed | Cooling group 4 configured | Installer group enable selection; not a cooling demand or active-service flag. |
| B71 | proposed | Cooling group 5 configured | Installer group enable selection; not a cooling demand or active-service flag. |
| B72 | deferred | Cooling group thermostat configuration/logic | gdNe_2 selector values lack verified option labels; not a demand flag. |
| B73 | deferred | Cooling group thermostat configuration/logic | gdNe_2 selector values lack verified option labels; not a demand flag. |
| B74 | deferred | Cooling group thermostat configuration/logic | gdNe_2 selector values lack verified option labels; not a demand flag. |
| B75 | deferred | Cooling group thermostat configuration/logic | gdNe_2 selector values lack verified option labels; not a demand flag. |
| B76 | deferred | Cooling group thermostat configuration/logic | gdNe_2 selector values lack verified option labels; not a demand flag. |
| B77 | proposed | Cooling group 1 curve selected | change() branches: 1 shows curve controls/image; 0 shows fixed-temperature controls/image. |
| B78 | proposed | Cooling group 2 curve selected | change() branches: 1 shows curve controls/image; 0 shows fixed-temperature controls/image. |
| B79 | proposed | Cooling group 3 curve selected | change() branches: 1 shows curve controls/image; 0 shows fixed-temperature controls/image. |
| B80 | proposed | Cooling group 4 curve selected | change() branches: 1 shows curve controls/image; 0 shows fixed-temperature controls/image. |
| B81 | proposed | Cooling group 5 curve selected | change() branches: 1 shows curve controls/image; 0 shows fixed-temperature controls/image. |
| B82 | proposed | Simultaneous heating and cooling consumption configured | Web label: Simultaneous consum. heating+cooling. This is not equal pool/buffer priority and does not promise simultaneous production or seamless changeover. |
| B83 | deferred | Auxiliary-system configuration or UI visibility flag | Used in show/hide conditions; some conditions differ across pages. Do not infer physical heater assignment or running state. |
| B84 | deferred | Auxiliary-system configuration or UI visibility flag | Used in show/hide conditions; some conditions differ across pages. Do not infer physical heater assignment or running state. |
| B85 | deferred | Auxiliary-system configuration or UI visibility flag | Used in show/hide conditions; some conditions differ across pages. Do not infer physical heater assignment or running state. |
| B86 | deferred | Floor-drying section visibility/configuration flag | Only a display condition; active floor phase is separately identified at 5089. |
| B89 | deferred | BUS room-terminal winter/summer function configuration | gd1e2 invokes habilitar_inv_ver; exact selector semantics need installer HTML. |
| B93 | deferred | Remote-control availability/configuration flag | Controls visibility of remote options; does not establish remote demand/input polarity. |
| B95 | deferred | Remote-control availability/configuration flag | Controls visibility of remote options; does not establish remote demand/input polarity. |
| B97 | deferred | Remote-control availability/configuration flag | Controls visibility of remote options; does not establish remote demand/input polarity. |
| B118 | deferred | Priority-page helper | Read into the array but no operational display or use was identified. |
| B119 | deferred | Priority-page Save yes/no field | Bound to save_yn. Treat as UI/save handshake, not a priority or changeover permission. |
| B122 | proposed | Cooling user enabled | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B123 | proposed | DHW recirculation user enabled | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B124 | proposed | DHW auxiliary 2 emergency enabled | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B125 | proposed | Pool auxiliary 2 emergency enabled | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B126 | proposed | Heating auxiliary 2 emergency enabled | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B127 | proposed | DHW auxiliary 2 support enabled | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B128 | proposed | Pool auxiliary 2 support enabled | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B129 | proposed | Heating auxiliary 2 support enabled | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B132 | proposed | Night mode enabled | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B133 | proposed | Legionella programme enabled | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B134 | proposed | Legionella Monday enabled | Day selection for the legionella schedule; does not mean the programme is running. |
| B135 | proposed | Legionella Tuesday enabled | Day selection for the legionella schedule; does not mean the programme is running. |
| B136 | proposed | Legionella Wednesday enabled | Day selection for the legionella schedule; does not mean the programme is running. |
| B137 | proposed | Legionella Thursday enabled | Day selection for the legionella schedule; does not mean the programme is running. |
| B138 | proposed | Legionella Friday enabled | Day selection for the legionella schedule; does not mean the programme is running. |
| B139 | proposed | Legionella Saturday enabled | Day selection for the legionella schedule; does not mean the programme is running. |
| B140 | proposed | Legionella Sunday enabled | Day selection for the legionella schedule; does not mean the programme is running. |
| B206 | proposed | Current summer season | principal.js selects summer for 1 and winter for 0. Numeric coil decoding is intentional; existing decoder does not support coil enums. |
| B212 | proposed | Automatic clock change enabled | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B213 | proposed | DHW user enabled | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B214 | deferred | DHW secondary control selector | en_acs_2 label references mf3.tdhw_control, missing from the captured translation. Do not guess enable/remote meaning. |
| B217 | deferred | Auxiliary-system configuration or UI visibility flag | Used in show/hide conditions; some conditions differ across pages. Do not infer physical heater assignment or running state. |
| B218 | proposed | DHW auxiliary 1 emergency enabled | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B219 | proposed | DHW auxiliary 1 support enabled | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B220 | deferred | Auxiliary-system configuration or UI visibility flag | Used in show/hide conditions; some conditions differ across pages. Do not infer physical heater assignment or running state. |
| B221 | proposed | Heating auxiliary 1 emergency enabled | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B222 | proposed | Heating auxiliary 1 support enabled | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B224 | proposed | Passive cooling production pump configured | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B225 | proposed | Passive cooling brine pump configured | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B226 | deferred | SG2..5 three-way-valve logic | gdNl selectors; polarity and codes need installer HTML. Not valve position feedback. |
| B227 | deferred | SG2..5 three-way-valve logic | gdNl selectors; polarity and codes need installer HTML. Not valve position feedback. |
| B228 | deferred | SG2..5 three-way-valve logic | gdNl selectors; polarity and codes need installer HTML. Not valve position feedback. |
| B229 | deferred | SG2..5 three-way-valve logic | gdNl selectors; polarity and codes need installer HTML. Not valve position feedback. |
| B232 | proposed | DHW recirculation event 1 state | Scheduled event action: 0 Off, 1 On. This is not a slot-enable flag or live pump state. |
| B233 | proposed | DHW recirculation event 2 state | Scheduled event action: 0 Off, 1 On. This is not a slot-enable flag or live pump state. |
| B234 | proposed | DHW recirculation event 3 state | Scheduled event action: 0 Off, 1 On. This is not a slot-enable flag or live pump state. |
| B235 | proposed | DHW recirculation event 4 state | Scheduled event action: 0 Off, 1 On. This is not a slot-enable flag or live pump state. |
| B249 | proposed | Anti frost enabled | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B252 | deferred | DHW-page unused read | No display or operational reference beyond the read was identified. |
| B262 | proposed | E-manager grid meter configured | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B263 | deferred | Grid connection selector | en_conexion under grid connection; option codes and phase interpretation unverified. |
| B264 | proposed | E-manager surplus control enabled | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B265 | proposed | E-manager consumption limit enabled | 0=no/disabled, 1=yes/enabled. Configuration readback, not pump/heater running feedback. Auxiliary controls can be hidden when the auxiliary is not configured. |
| B266 | proposed | E-manager surplus control status | Principal page shows Off for 0 and On for 1. Do not equate this with compressor or heater running. |
| B267 | proposed | E-manager consumption limit status | Principal page shows Off for 0 and On for 1. Do not equate this with compressor or heater running. |
| I5008 | deferred | Compressor total starts display components | Web concatenates 5008 and a four-digit 5009; likely 5008*10000+5009. JS has a padding/index bug; rollover, reset and counter semantics need validation. |
| I5009 | deferred | Compressor total starts display components | Web concatenates 5008 and a four-digit 5009; likely 5008*10000+5009. JS has a padding/index bug; rollover, reset and counter semantics need validation. |
| I5010 | deferred | Compressor operating hours display components | Web concatenates two three-digit parts; likely 5010*1000+5011 hours. Validate rollover/reset and the controller screen before publishing a total-increasing sensor. |
| I5011 | deferred | Compressor operating hours display components | Web concatenates two three-digit parts; likely 5010*1000+5011 hours. Validate rollover/reset and the controller screen before publishing a total-increasing sensor. |
| I5012 | deferred | Compressor starts/hour integer display component | Combined with existing 5013 fractional component. Observed signed integer -4 and fraction 881 are implausible for a rate; retain as investigation evidence only. |
| I5027 | deferred | Heating group emitter type | gdNe selector; complete option/code mapping not recovered. |
| I5028 | deferred | Heating group emitter type | gdNe selector; complete option/code mapping not recovered. |
| I5029 | deferred | Heating group emitter type | gdNe selector; complete option/code mapping not recovered. |
| I5030 | deferred | Heating group emitter type | gdNe selector; complete option/code mapping not recovered. |
| I5031 | deferred | Heating group emitter type | gdNe selector; complete option/code mapping not recovered. |
| I5032 | deferred | Building insulation selection | Label and Good/Moderate/Bad translations exist; option/code mapping not recovered. |
| I5033 | deferred | Cooling connection type | Connection-type selector and conditional branches exist; complete code/label mapping not recovered. |
| I5034 | deferred | Cooling group emitter type | gdNe selector; complete option/code mapping not recovered. |
| I5035 | deferred | Cooling group emitter type | gdNe selector; complete option/code mapping not recovered. |
| I5036 | deferred | Cooling group emitter type | gdNe selector; complete option/code mapping not recovered. |
| I5037 | deferred | Cooling group emitter type | gdNe selector; complete option/code mapping not recovered. |
| I5038 | deferred | Cooling group emitter type | gdNe selector; complete option/code mapping not recovered. |
| I5045 | proposed | Floor drying phase 1 duration hours | Installer information page displays h for the selected phase. Not a service time allocation. |
| I5046 | proposed | Floor drying phase 2 duration hours | Installer information page displays h for the selected phase. Not a service time allocation. |
| I5047 | proposed | Floor drying phase 3 duration hours | Installer information page displays h for the selected phase. Not a service time allocation. |
| I5048 | proposed | Floor drying phase 4 duration hours | Installer information page displays h for the selected phase. Not a service time allocation. |
| I5049 | proposed | Floor drying phase 5 duration hours | Installer information page displays h for the selected phase. Not a service time allocation. |
| I5050 | proposed | Floor drying phase 6 duration hours | Installer information page displays h for the selected phase. Not a service time allocation. |
| I5052 | deferred | Priority-page extra integer | Read but no display/operational use identified; cannot name it as priority/time allocation. |
| I5061 | proposed | Web operating state | principal.js state icon mapping; distinct encoding from user-panel state 5062. |
| I5062 | proposed | User panel operating selection | on_off.html selector; selection is not proof the compressor is running. |
| I5063 | proposed | Season programme code | on_off.html: 0 Winter, 1 Summer, 2 Auto, 4 Remote. Option 3 references a translation missing from the captured English file, so its meaning is not asserted. |
| I5064 | proposed | Automatic season change delay hours | on_off.html explicitly displays h with bounds 0..8. Seasonal delay, not compressor restart delay. |
| I5065 | proposed | Night start hour | Hour/minute inferred from HTML position and 0..23/0..59 input bounds, not misleading min_ini/hor_ini IDs. No date/timezone inference. |
| I5066 | proposed | Night start minute | Hour/minute inferred from HTML position and 0..23/0..59 input bounds, not misleading min_ini/hor_ini IDs. No date/timezone inference. |
| I5067 | proposed | Night end hour | Hour/minute inferred from HTML position and 0..23/0..59 input bounds, not misleading min_ini/hor_ini IDs. No date/timezone inference. |
| I5068 | proposed | Night end minute | Hour/minute inferred from HTML position and 0..23/0..59 input bounds, not misleading min_ini/hor_ini IDs. No date/timezone inference. |
| I5069 | proposed | Night compressor capacity limit | calendario.html displays % and input range 25..100; configured limit, not actual RPM. |
| I5070 | proposed | Legionella start hour | Hour/minute inferred from HTML position and 0..23/0..59 input bounds, not misleading min_ini/hor_ini IDs. No date/timezone inference. |
| I5071 | proposed | Legionella start minute | Hour/minute inferred from HTML position and 0..23/0..59 input bounds, not misleading min_ini/hor_ini IDs. No date/timezone inference. |
| I5077 | proposed | Cooling group 1 user adjustment | frio_usuario.html boost options: codes 0..4 correspond to -4,-2,0,+2,+4 degrees C. |
| I5078 | proposed | Cooling group 2 user adjustment | frio_usuario.html boost options: codes 0..4 correspond to -4,-2,0,+2,+4 degrees C. |
| I5079 | proposed | Cooling group 3 user adjustment | frio_usuario.html boost options: codes 0..4 correspond to -4,-2,0,+2,+4 degrees C. |
| I5080 | proposed | Cooling group 4 user adjustment | frio_usuario.html boost options: codes 0..4 correspond to -4,-2,0,+2,+4 degrees C. |
| I5081 | proposed | Cooling group 5 user adjustment | frio_usuario.html boost options: codes 0..4 correspond to -4,-2,0,+2,+4 degrees C. |
| I5089 | proposed | Floor drying phase | 0 inactive; phases 1..6 select their corresponding duration registers. Not compressor/service phase. |
| I5090 | proposed | Floor drying phase elapsed hours | Web display shows h only when 5089 is nonzero. Do not treat a retained value as active runtime. |
| I5102 | proposed | Automatic clock change offset minutes | calendario.html dia1 displays min and input range 0..240. |
| I5103 | proposed | Automatic clock change start week | Calendar option values; ordinal occurrence of the selected weekday, not week number. |
| I5104 | proposed | Automatic clock change start weekday | 0 unset; 1 Monday through 7 Sunday. |
| I5105 | proposed | Automatic clock change start month | 0 unset; 1 January through 12 December. |
| I5106 | proposed | Automatic clock change start hour | Local controller hour 0..23; timezone not identified. |
| I5107 | proposed | Automatic clock change end week | Calendar option values; ordinal occurrence of the selected weekday, not week number. |
| I5108 | proposed | Automatic clock change end weekday | 0 unset; 1 Monday through 7 Sunday. |
| I5109 | proposed | Automatic clock change end month | 0 unset; 1 January through 12 December. |
| I5110 | proposed | Automatic clock change end hour | Local controller hour 0..23; timezone not identified. |
| I5149 | deferred | BUS room-terminal compensation parameters | rca/rcb fields in heating/cooling; precise unit and association with DT S/W Off/On not verified. |
| I5150 | deferred | BUS room-terminal compensation parameters | rca/rcb fields in heating/cooling; precise unit and association with DT S/W Off/On not verified. |
| I5151 | deferred | BUS room-terminal compensation parameters | rca/rcb fields in heating/cooling; precise unit and association with DT S/W Off/On not verified. |
| I5152 | deferred | BUS room-terminal compensation parameters | rca/rcb fields in heating/cooling; precise unit and association with DT S/W Off/On not verified. |
| I5153 | deferred | BUS room-terminal compensation parameters | rca/rcb fields in heating/cooling; precise unit and association with DT S/W Off/On not verified. |
| I5154 | deferred | BUS room-terminal compensation parameters | rca/rcb fields in heating/cooling; precise unit and association with DT S/W Off/On not verified. |
| I5155 | deferred | BUS room-terminal compensation parameters | rca/rcb fields in heating/cooling; precise unit and association with DT S/W Off/On not verified. |
| I5156 | deferred | BUS room-terminal compensation parameters | rca/rcb fields in heating/cooling; precise unit and association with DT S/W Off/On not verified. |
| I5157 | deferred | BUS room-terminal compensation parameters | rca/rcb fields in heating/cooling; precise unit and association with DT S/W Off/On not verified. |
| I5158 | deferred | BUS room-terminal compensation parameters | rca/rcb fields in heating/cooling; precise unit and association with DT S/W Off/On not verified. |
| I5164 | proposed | DHW recirculation event 1 hour | acs_usuario.html schedule input and bounds; paired with the event On/Off action coil. |
| I5165 | proposed | DHW recirculation event 1 minute | acs_usuario.html schedule input and bounds; paired with the event On/Off action coil. |
| I5166 | proposed | DHW recirculation event 2 hour | acs_usuario.html schedule input and bounds; paired with the event On/Off action coil. |
| I5167 | proposed | DHW recirculation event 2 minute | acs_usuario.html schedule input and bounds; paired with the event On/Off action coil. |
| I5168 | proposed | DHW recirculation event 3 hour | acs_usuario.html schedule input and bounds; paired with the event On/Off action coil. |
| I5169 | proposed | DHW recirculation event 3 minute | acs_usuario.html schedule input and bounds; paired with the event On/Off action coil. |
| I5170 | proposed | DHW recirculation event 4 hour | acs_usuario.html schedule input and bounds; paired with the event On/Off action coil. |
| I5171 | proposed | DHW recirculation event 4 minute | acs_usuario.html schedule input and bounds; paired with the event On/Off action coil. |
| I5329 | proposed | E-manager grid meter address | emanager_instalador direccion under GRID METER. Numeric configured address; does not prove a meter is connected. |
| I5330 | deferred | E-manager activation/deactivation times | t_activacion/t_desactivacion names clear; seconds versus minutes not established. |
| I5331 | deferred | E-manager activation/deactivation times | t_activacion/t_desactivacion names clear; seconds versus minutes not established. |
