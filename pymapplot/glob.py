# X_RANGE = [-87.687150, -87.639896]
# Y_RANGE = [41.861952,   41.883565]

# zoom level 15
# X_RANGE = [-87.677256, -87.649790]
# Y_RANGE = [41.862532, 41.882984]

# zoom level 14
# X_RANGE = [-87.690989, -87.636057]
# Y_RANGE = [41.852303, 41.893207]

# zoom: 17 for example 1!!!
# X_MOVE = -0.01
# Y_MOVE = -0.002

X_MOVE =  0.015
Y_MOVE = -0.005
X_RANGE = [-87.690989 + X_MOVE, -87.636057 + X_MOVE]
Y_RANGE = [41.852303  + Y_MOVE,  41.893207 + Y_MOVE]

ROOT_DIR = '/Users/hengfeng/github-2/map-inference/'
CLUSTERED_POINTS_FILE = ROOT_DIR + 'clusterd_gps_point.txt'
DATA_DIR = ROOT_DIR + 'data/chicago/'
TRAJ_PATH = DATA_DIR + 'trips/'
# MAP_DIR = "test_data/shrink-road-maps/"
MAP_DIR = DATA_DIR + 'maps_chicago_reduced/'
TRAJ_FILE_RANGE = [0, 0]

# Melbourne
# X_RANGE = [144.968, 145.050]
# Y_RANGE = [-37.819, -37.755]
#
# DATA_DIR = '/Users/hengfeng/github-2/map-inference/data/melb/'
# TRAJ_PATH = DATA_DIR + 'trips/'
# MAP_DIR = DATA_DIR + 'map_melb_reduced/'
# TRAJ_FILE_RANGE = [0, 9999]

MY_DPI = 96
SCALE = 1
PIC_WIDTH = 1280 * SCALE
LINEWIDTH = 4

# three good cases
# POS_X = 250 * SCALE
# POS_Y = 260 * SCALE
# AREA_SIZE = 150 * SCALE

# POS_X = 750 * SCALE
# POS_Y = 270 * SCALE
# AREA_SIZE = 150 * SCALE

# POS_X = 720 * SCALE
# POS_Y = 330 * SCALE
# AREA_SIZE = 150 * SCALE

POS_X = 0 * SCALE
POS_Y = 0 * SCALE
X_SPAN = 300
Y_SPAN = 300