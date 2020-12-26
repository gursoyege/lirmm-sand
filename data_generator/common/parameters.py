#action = "poke_16times_loSand"
#action = "grasp_4times_hiSand"
#action = "grasp_4times_hiSand2"
#action = "tap_4times_hiSand"
#action = "tap_4times_hiSand2"
#action = "tap_8times_loSand"

#action = "poke"
action = "tap"
#action = "grasp"


nSample = 100

train_test_ratio = 12 #7/10

ANNOTATION_PATH = "resource/annotation/" + action
IMAGE_PATH = "resource/image/" + action
XML_PATH = "output/annotation/" + action
DATA_PATH = "output/class/" + action
AUGMENT_PATH = "output/data/" + action
R_PATH = "output/r_value/" + action

U0 = 424
V0 = 240
FX = 415
FY = 373
IM_SIZE = (848,480)