# LIRMM-sand

Sand manipulation project.
Please check the project report in the directory "/lirmm-sand_report.pdf" for more detailed explanaiton.

## Prerequisites


```
python v3.6 (or greater) 
opencv v4.0 (not tested on other versions)
tensorflow v2.2 (or greater)
numpy
lxml
```
Pre-trained autoencoder models can be downloaded using the link below :
https://drive.google.com/drive/folders/1yB7gM8_BIdyEDKX69TVZK8chWw2lKNVy?usp=sharing

Downloaded "model" folder should be placed under :
```
decision_tree/resources/
```

## Usage

Clone the master branch repository. Then, set desired parameters in :

```
data_augmentor/common/parameters.py
```
```
action # action to be performed.
nSample # number of sample images to be generated for each image of the beginning and ending of an action.
*_PATH # locations of the folders to be generated.
```
Desired actions can be set by commenting out the modules in :
```
data_augmentor.py
```

Launch the data_augmentor package.

```
cd data_augmentor
python -m data_generator
```
Data for the selected action will be created under :
```
/data_augmentor/output/data
```
### Notes

Some explications about the structure of the project :

```
resource/image : raw image data coming from the camera.
resource/annotation : annotions of the beginning or ending of an action which contain the name of the action, name of the related image and region of interest.
```
```
output/annotation : annotations of the images to be generated and to be classed as the beginning and ending of an action.
output/class : classified images as the beginning or ending of an action, then cropped down to the average area of the region of interests of that action.
output/data : artificially generated images from the class data.
```
All the output data structured as follows :
```
<action>/beg : denotes the beggining of the <action>
<action>/end : denotes the ending of the <action>
```
Image augmentation methods :
```
rotate : rotation with added black padding.
flipH : horizontal flip.
flipV : vertical flip.
zoom : zoom to the center of the image.
translate : translation with added black padding.
bright : brightness adjustement.
contrast : contrast adjustement.
gauss : add gaussian distributed noise.
saltPep : add salt and pepper noise.
poisson : add poisson distributed noise.
speckle : add speckle noise.
```
Then, a pipeline consists of all the augmentation methods with different probabilities are initialized with random values. "nSample" of artificial images are generated for each image.

#### Example

```
# Raw image coming from the camera:
resource/image/tap/image0012.png
# Annotation of the image manually created.
resource/annotation/tap/image0012.xml
# Image classified as the '4th example' of the 'beginning' of the '3rd instance' of the 'tap' action then the annotation data is generated.
output/annotation/tap/begin/3beg_4.xml
# Cropped image generated according to the annotation file.
output/class/tap/begin/3beg/3beg_4.jpg
# Image is augmented and the '71th' augmented image is generated.
output/data/tap/begin/3beg/3beg_4_71.jpg
```
