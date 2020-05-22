from imports import *
import xml_generator, image_verifier, image_cropper

xml_generator.clean()
image_cropper.clean()

xml_generator.run()
image_verifier.run()
image_cropper.run()