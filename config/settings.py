# Path to the root location of the application. When app is run inside
# a container (the default) this is container-relative (e.g. '/qmview')
APP_ROOT = '/qmview'

# Configuration directory, inside the application
CONFIG_DIR = "{}/config".format(APP_ROOT)

# Logging level
LOG_LEVEL = 'INFO'  # CRITICAL / ERROR / WARNING / INFO / DEBUG

# Name of this program: used programmatically so keeping it lower case.
PROGRAM_NAME = 'qmview'

# Path to the default output reports directory.
REPORTS_DIR = 'reports'
