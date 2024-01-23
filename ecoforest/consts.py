import httpx

URL_CGI = "/recepcion_datos_4.cgi"

LOCAL_TIMEOUT = httpx.Timeout(
    # The device can be slow to respond but fast to connect to we
    # need to set a long timeout for the read and a short timeout
    # for the connect
    timeout=10.0,
    read=60.0,
)

DIGITAL_READINGS_MAPPINGS = {
    'POOL_PRESENT': 62,
    'POOL_ENABLED': 215,
    'POOL_USE_REMOTE_SWITCH': 216,

}

ANALOGUE_READINGS_MAPPINGS = {

    # Temperature input brine
    "TIP_a": 1,
    # Temperature return brine
    "TRP_a": 2,

    # Temperature climate input
    "TIC_a": 4,
    # Tempereature climate return
    "TRC_a": 5,

    # Pressure, climate XXX ?
    "PCP_a": 3,
    # Pressure, climate XXX ?
    "PCC_a": 6,

    # DHW REal temp
    "temp_acum_acs": 11,
    # DHW DT start
    "offset": 41,
    # DHW Set temp
    "consigna_acs": 38,

    # DHW recirculation set point
    "retorno_setp": 42,
    # DHW recirculation real temp
    "retorno": 12,
    # DT start DHW recirculation
    "dtretorno": 43,

    # Heating stop tempature
    'temp_cal': 44,
    'temp_ref': 66,
    'temp_ref_act': 67,

    # Set (point) temperatures
    'set_th1': 123,
    'set_th2': 124,
    'set_th3': 125,
    'set_th4': 126,
    'set_th5': 127,

    'set_th1_1': 128,
    'set_th2_1': 129,
    'set_th3_1': 130,
    'set_th4_1': 131,
    'set_th5_1': 132,

    # Real temperatures
    'real_t_th1': 21,
    'real_t_th2': 13,
    'real_t_th3': 14,
    'real_t_th4': 15,
    'real_t_th5': 16,

    # ???
    'reg_th2': 31,
    'reg_th3': 32,
    'reg_th4': 33,
    'reg_th5': 34,

    "temp_exterior": 20,

    'energ_util_heat': 133,
    'energ_util_cool': 134,
    'ELECTRICITY_USE': 135,
    'cop_value': 136,
    'eer_value': 137,
    'pf_value': 138,

    "c_dg1": 151,
    "c_dg2": 152,
    "c_dg3": 153,
    "c_dg4": 154,
    "c_dg5": 155,
    "d_dg1": 161,
    "d_dg2": 162,
    "d_dg3": 163,
    "d_dg4": 164,
    "d_dg5": 165,

    # Real temp
    "temp_acum_pool": 19,
    # Pool set temp
    "setpoint_pool": 119,
    # DT start pool
    "offset_pool": 120,

}