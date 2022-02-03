# Proxmox
from proxmoxer import ProxmoxAPI

# Netbox
import pynetbox

# Default Plugins settings 
from netbox_proxbox import ProxboxConfig

# PLUGIN_CONFIG variable defined by user in Netbox 'configuration.py' file
from netbox.settings import PLUGINS_CONFIG

####################################################################################################
#                                                                                                  #
#  DEFAULT VARIABLES DEFINED BY ProxboxConfig CLASS ON PROXBOX PLUGIN CONFIGURATION (__init__.py)  #
#                                                                                                  #
####################################################################################################

DEFAULT_PLUGINS_CONFIG = ProxboxConfig.default_settings
# DEFAULT_PROXMOX_SETTING = DEFAULT_PLUGINS_CONFIG.get("proxmox")
DEFAULT_PROXMOX_SETTING = {
    'domain': 'proxbox.example.com',  # May also be IP address
    'http_port': 8006,
    'user': 'root@pam',
    'password': 'Strong@P4ssword',
    'token': {
        'name': 'tokenID',
        'value': '039az154-23b2-4be0-8d20-b66abc8c4686'
    },
    'ssl': False
}

DEFAULT_NETBOX_SETTING = DEFAULT_PLUGINS_CONFIG.get("netbox")

#
# Proxmox related settings
#
# API URI
DEFAULT_PROXMOX = DEFAULT_PROXMOX_SETTING.get("domain")
DEFAULT_PROXMOX_PORT = DEFAULT_PROXMOX_SETTING.get("http_port")
DEFAULT_PROXMOX_SSL = DEFAULT_PROXMOX_SETTING.get("ssl")

# ACCESS
DEFAULT_PROXMOX_USER = DEFAULT_PROXMOX_SETTING.get("user")
DEFAULT_PROXMOX_PASSWORD = DEFAULT_PROXMOX_SETTING.get("password")

DEFAULT_PROXMOX_TOKEN = DEFAULT_PROXMOX_SETTING.get("token")
DEFAULT_PROXMOX_TOKEN_NAME = DEFAULT_PROXMOX_TOKEN.get("name", None)
DEFAULT_PROXMOX_TOKEN_VALUE = DEFAULT_PROXMOX_TOKEN.get("value", None)

#
# NETBOX RELATED SETTINGS
#
# API URI
#
DEFAULT_NETBOX = DEFAULT_NETBOX_SETTING.get("domain")
DEFAULT_NETBOX_PORT = DEFAULT_NETBOX_SETTING.get("http_port")
DEFAULT_NETBOX_SSL = DEFAULT_NETBOX_SETTING.get("ssl")

# ACCESS
DEFAULT_NETBOX_TOKEN = DEFAULT_NETBOX_SETTING.get("token")

# SETTINGS
DEFAULT_NETBOX_SETTINGS = DEFAULT_NETBOX_SETTING.get("settings")
DEFAULT_NETBOX_VM_ROLE_ID = DEFAULT_NETBOX_SETTINGS.get("virtualmachine_role_id", 0)
DEFAULT_NETBOX_NODE_ROLE_ID = DEFAULT_NETBOX_SETTINGS.get("node_role_id", 0)
DEFAULT_NETBOX_SITE_ID = DEFAULT_NETBOX_SETTINGS.get("site_id", 0)

####################################################################################################
#                                                                                                  #
#         VARIABLES FROM PLUGINS_CONFIG DEFINED BY USER ON NETBOX configuration.py                 #
#                                                                                                  #
####################################################################################################

# Get Proxmox credentials values from PLUGIN_CONFIG
USER_PLUGINS_CONFIG = PLUGINS_CONFIG.get("netbox_proxbox")
PROXMOX_SETTING = USER_PLUGINS_CONFIG.get("proxmox", DEFAULT_PROXMOX_SETTING)
NETBOX_SETTING = USER_PLUGINS_CONFIG.get("netbox", DEFAULT_NETBOX_SETTING)

#
# NETBOX RELATED SETTINGS
#
# API URI
#
NETBOX = NETBOX_SETTING.get("domain", DEFAULT_NETBOX)
NETBOX_PORT = NETBOX_SETTING.get("http_port", DEFAULT_NETBOX_PORT)
NETBOX_SSL = NETBOX_SETTING.get("ssl", DEFAULT_NETBOX_SSL)

# ACCESS
NETBOX_TOKEN = NETBOX_SETTING.get("token", DEFAULT_NETBOX_TOKEN)

# SETTINGS
NETBOX_SETTINGS = NETBOX_SETTING.get("settings", DEFAULT_NETBOX_SETTINGS)

if NETBOX_SETTINGS != None:
    NETBOX_VM_ROLE_ID = NETBOX_SETTINGS.get("virtualmachine_role_id", DEFAULT_NETBOX_VM_ROLE_ID)
    NETBOX_NODE_ROLE_ID = NETBOX_SETTINGS.get("node_role_id", DEFAULT_NETBOX_NODE_ROLE_ID)
    NETBOX_SITE_ID = NETBOX_SETTINGS.get("site_id", DEFAULT_NETBOX_SITE_ID)

PROXMOX_SESSIONS = {}


def get_proxmox_session(PROXMOX_SETTING):
    #
    # Proxmox related settings
    #
    # API URI

    PROXMOX = PROXMOX_SETTING.get("domain", DEFAULT_PROXMOX)
    PROXMOX_PORT = PROXMOX_SETTING.get("http_port", DEFAULT_PROXMOX_PORT)
    PROXMOX_SSL = PROXMOX_SETTING.get("ssl", DEFAULT_PROXMOX_SSL)

    # ACCESS
    PROXMOX_USER = PROXMOX_SETTING.get("user", DEFAULT_PROXMOX_USER)
    PROXMOX_PASSWORD = PROXMOX_SETTING.get("password", DEFAULT_PROXMOX_PASSWORD)

    PROXMOX_TOKEN = PROXMOX_SETTING.get("token", DEFAULT_PROXMOX_TOKEN)
    if PROXMOX_TOKEN != None:
        PROXMOX_TOKEN_NAME = PROXMOX_TOKEN.get("name", DEFAULT_PROXMOX_TOKEN_NAME)
        PROXMOX_TOKEN_VALUE = PROXMOX_TOKEN.get("value", DEFAULT_PROXMOX_TOKEN_VALUE)
    output = {
        'PROXMOX': PROXMOX,
        'PROXMOX_PORT': PROXMOX_PORT,
        'PROXMOX_SSL': PROXMOX_SSL,
        'PROXMOX_TOKEN': PROXMOX_TOKEN,
        'PROXMOX_TOKEN_NAME': PROXMOX_TOKEN_NAME,
        'PROXMOX_TOKEN_VALUE': PROXMOX_TOKEN_VALUE
    }
    ####################################################################################################
    #                                                                                                  #
    #                 WITH PLUGIN CONFIGURED, STARTS BOTH PROXMOX AND NETBOX SESSION                   #
    #                                                                                                  #
    ####################################################################################################

    #
    # PROXMOX SESSION
    #
    # Check if token was provided
    if PROXMOX_TOKEN_VALUE != None and len(PROXMOX_TOKEN_VALUE) > 0:
        try:
            # Start PROXMOX session using TOKEN
            PROXMOX_SESSION = ProxmoxAPI(
                PROXMOX,
                user=PROXMOX_USER,
                token_name=PROXMOX_TOKEN_NAME,
                token_value=PROXMOX_TOKEN_VALUE,
                verify_ssl=PROXMOX_SSL
            )
            output['PROXMOX_SESSION'] = PROXMOX_SESSION
            return output
        except:
            print('Error trying to initialize Proxmox Session using TOKEN provided')
    return None


for s in PROXMOX_SETTING:
    P_Setting = get_proxmox_session(s)
    if P_Setting is not None:
        v = P_Setting['PROXMOX']
        PROXMOX_SESSIONS[v] = P_Setting

#
# NETBOX SESSION 
#
if NETBOX_SSL == False:
    try:
        NETBOX = 'http://{}:{}'.format(NETBOX, NETBOX_PORT)
        # Inicia sessão com NETBOX
        NETBOX_SESSION = pynetbox.api(
            NETBOX,
            token=NETBOX_TOKEN
        )
    except:
        print('Error trying to initialize Netbox Session using TOKEN provided')
elif NETBOX_SSL == True:
    print("Netbox using SSL not developed yet, try using HTTP without SSL.")

else:
    print('Unexpected Error ocurred')
