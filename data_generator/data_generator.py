from common.imports import *
from module import tree_generator, xml_generator, image_cropper, data_augmenter

''' FUTURE:
    1 - Generate all actions in single program
    2 - Raw image annotation generator
'''

xml_generator.clean()
image_cropper.clean()
data_augmenter.clean()

tree_generator.run()
xml_generator.run()
# image_verifier.run()
image_cropper.run()
data_augmenter.run()
