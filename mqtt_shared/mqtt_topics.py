CONNECT = 'BananaBreadSmartOven/connect'
DISCONNECT = 'BananaBreadSmartOven/disconnect'

################

PREFIX = 'BananaBreadSmartOven/{device_id}'

INFO_PREFIX = f'{PREFIX}/info'

# constantly send data from temperature sensor
TEMPERATURE = f'{INFO_PREFIX}/temperature'

# constantly send to server info about current recipe
RECIPE_DETAILS = f'{INFO_PREFIX}/recipe_details'

################

SETTINGS_PREFIX = f'{PREFIX}/settings'

# send instructions to change device state
STATE = f'{SETTINGS_PREFIX}/state'
