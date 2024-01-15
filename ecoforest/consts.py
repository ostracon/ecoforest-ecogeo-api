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
    'POOL_ENABLED': 62
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

    'energ_util_heat': 133,
    'energ_util_cool': 134,
    'ELECTRICITY_USE': 135,
    'cop_value': 136,
    'eer_value': 137,
    'pf_value': 138
}