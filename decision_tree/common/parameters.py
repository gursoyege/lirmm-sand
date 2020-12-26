import numpy as np

l_max = 3
k_max = 20
d_thres = 0

#ACTIONS = ["poke_16times_loSand", "grasp_4times_hiSand", "tap_4times_hiSand", "tap_8times_loSand"]

#ACTIONS = ["poke_16times_loSand"]

ACTIONS = ["tap"]

IM_SIZE = (848,480)
U0 = 424
V0 = 240
FX = 415
FY = 373

r_max = np.sqrt(1 + (U0/FX)**2 + (V0/FY)**2)

GRID_SIZE = (2,2)
BLEND_RATE = 10

INIT_PATH = "resource/initial/"
DESIR_PATH = "resource/desired/"
TREE_PATH = "output/tree/"
MODEL_PATH = "resource/model/"
SEQUENCE_PATH = "output/sequence/"
ANNOTATION_PATH = "resource/annotation/"