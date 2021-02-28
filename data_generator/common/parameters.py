#action = "fist"
#action = "grasp"
action = "poke"

nSample = 6

train_test_ratio = 75 #3/4


ANNOTATION_PATH = "resource/annotation/" + action
IMAGE_PATH = "resource/image/" + action
XML_PATH = "output/annotation/" + action
BATCH_PATH = "resource/batch/" + action
DATA_PATH = "output/class/" + action
AUGMENT_PATH = "output/data/" + action
R_PATH = "output/r_value/" + action

U0 = 424
V0 = 240
FX = 415
FY = 373
IM_SIZE = (848,480)

