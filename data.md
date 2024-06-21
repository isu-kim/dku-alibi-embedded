# Dataset Description

## 1. Dataset Overview
This dataset consists of photos of faces collected directly for learning face recognition models. It consists of a total of nine classes (people), each of which represents a specific person. All photos were taken directly or downloaded from the internet, and manually labeled using LabelMe.

## 2. Number of Data
The dataset contains a total of 119 images. The number of images per class is as follows:

- doik: 26 sheets
- IU: 20 sheets
- minjung: 10 sheets
- rose: 10 sheets
- shokhrukh: 10 sheets
- yeji: 10 sheets
- isu: 10 sheets
- zabo: 13 sheets
- jisoo: 10 sheets

## 3. Label Type
There are a total of nine labels in the dataset, each class representing a specific person:

- doik
- IU
- minjung
- rose
- shokhrukh
- yeji
- isu
- zabo
- jisoo

The label is defined in the `dataset.yaml` file and is organized in the following format:


nc: 9
names: ["doik", "IU", "minjung", "rose", "shokhrukh", "yeji", "isu", "zabo", "jisoo"]


## 4. How to Collect Data

Except for celebrities, the data was collected by taking direct facial photos. About 10 to 20 images were taken for each class, and the images were taken in high resolution. The images taken were prepared through the following process:

### Photography
Face photos were taken from various facial expressions and angles of each character.

### Labeling
Images taken were manually labeled using the LabelMe tool. For each image, we designated the face area as a bounding box and assigned a class to that bounding box.

### Dataset Configuration
Labeled images were organized in the `images` folder and converted to YOLO format using the `labelme2yolo` script. During the conversion process, 20% of the dataset was separated as validation data and 10% as test data.

### Resize the Image
All images were adjusted to 640x640 pixels size to suit YOLO model training.

## 5. Learning Process
This dataset was used to train the YOLO model, and the training was conducted for 100 epochs. During the learning process, the performance of the model was periodically verified and the final model was saved.

