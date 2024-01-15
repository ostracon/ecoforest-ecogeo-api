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