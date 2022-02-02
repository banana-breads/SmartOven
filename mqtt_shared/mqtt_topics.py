CONNECT = 'BananaBreadSmartOven/connect'
DISCONNECT = 'BananaBreadSmartOven/disconnect'

PREFIX = 'BananaBreadSmartOven/{device_id}'

################

INFO_PREFIX = f'{PREFIX}/info'

# constantly send data from sensors
TEMPERATURE = f'{INFO_PREFIX}/temperature'

TIME = f'{INFO_PREFIX}/time'

STATE = f'{INFO_PREFIX}/state'

# send to server info about current recipe
RECIPE_DETAILS = f'{INFO_PREFIX}/recipe_details'

RECIPE_DONE = f'{INFO_PREFIX}/recipe_done'

################

SETTINGS_PREFIX = f'{PREFIX}/settings'

# send instructions to change device state
SET_STATE = f'{SETTINGS_PREFIX}/set_state'
# send instructions to set oven parameters according to 
# a specific recipe (temperature, cooking duration, description)
SET_RECIPE = f'{SETTINGS_PREFIX}/set_recipe'
# send instructions to change oven temperature
SET_TEMPERATURE = f'{SETTINGS_PREFIX}/set_temperature'
# send instructions to change oven cooking time
SET_TIME = f'{SETTINGS_PREFIX}/set_time'

################

REQUEST_PREFIX = f'{PREFIX}/request/'

GET_RECIPE_DETAILS = f'{REQUEST_PREFIX}/get_recipe_details'
