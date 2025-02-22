"""
This file contains the pluggable component for the transport
"""

import requests
from config_reader import ConfigReader

from config_private import APM_PUBLIC_KEY

#
# general configs
#
config = ConfigReader("config.toml")

#
# configs for zipkin transport
# see notes here:
# https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/configure-open-source-tracing-systems.html
#
BASE_URL = config.find_key("apm_base_url")
APM_CONTENT_TYPE = config.find_key("apm_content_type")
# in config.toml we can enable/disable globally tracing
ENABLE_TRACING = config.find_key("enable_tracing")

# this is the public endpoint we're calling
APM_UPLOAD_ENDPOINT_URL = f"{BASE_URL}/observations/public-span?dataFormat=zipkin&dataFormatVersion=2&dataKey={APM_PUBLIC_KEY}"


def http_transport(encoded_span):
    """
    This function gives the pluggable transport
    to communicate with OCI APM using py-zipkin
    """
    result = None

    if ENABLE_TRACING:
        result = requests.post(
            APM_UPLOAD_ENDPOINT_URL,
            data=encoded_span,
            headers={"Content-Type": APM_CONTENT_TYPE},
            timeout=10,
        )
    return result
