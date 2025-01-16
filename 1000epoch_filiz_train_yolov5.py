# -*- coding: utf-8 -*-
"""1000epoch_Filiz_Train_YOLOv5

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dMr7vD4si_G6CRvXXyfl9m0zroAlUjDh
"""

# Commented out IPython magic to ensure Python compatibility.
# clone YOLOv5 repository
#To train our detector we take the following steps:
#Install YOLOv5 dependencies
#Download custom YOLOv5 object detection data
!git clone https://github.com/ultralytics/yolov5  # clone repo
# %cd yolov5
!git reset --hard 886f1c03d839575afecb059accf74296fad395b6

from google.colab import drive
drive.mount('/content/drive')
# drive hesabından gerekli veriseti ve dosyaların path tanımlama ile alınabilmesi için account mounting

!unzip -q /content/drive/MyDrive/data_yeni_sar.zip -d /content

# install dependencies as necessary
!pip install -qr requirements.txt  # install dependencies (ignore errors)
import torch

from IPython.display import Image, clear_output  # to display images
from utils.google_utils import gdrive_download  # to download models/datasets

# clear_output()
print('Setup complete. Using torch %s %s' % (torch.__version__, torch.cuda.get_device_properties(0) if torch.cuda.is_available() else 'CPU'))

#follow the link below to get your download code from from Roboflow
!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="1GjZiWAlvNWii0xwIUOI")
project = rf.workspace("filiz_yildiz26-hotmail-com").project("sar_training_vol1")
dataset = project.version(1).download("yolov5")

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/yolov5
#after following the link above, recieve python code with these fields filled in
#from roboflow import Roboflow
#rf = Roboflow(api_key="YOUR API KEY HERE")
#project = rf.workspace().project("YOUR PROJECT")
#dataset = project.version("YOUR VERSION").download("yolov5")

# Commented out IPython magic to ensure Python compatibility.
# this is the YAML file Roboflow wrote for us that we're loading into this notebook with our data
# %cat {dataset.location}/data.yaml

#Define Model Configuration and Architecture
# with script that defines the parameters for our model like the number of classes
import yaml
# define number of classes based on YAML
with open(dataset.location + "/data.yaml", 'r') as stream:
    num_classes = str(yaml.safe_load(stream)['nc'])

# Commented out IPython magic to ensure Python compatibility.
#this is the model configuration we will use for our tutorial
#YAML file defining where SAR training and test data is
# %cat /content/yolov5/models/yolov5s.yaml

#customize iPython writefile so we can write variables
from IPython.core.magic import register_line_cell_magic

@register_line_cell_magic
def writetemplate(line, cell):
    with open(line, 'w') as f:
        f.write(cell.format(**globals()))

# Commented out IPython magic to ensure Python compatibility.
# %%writetemplate /content/yolov5/models/custom_yolov5s.yaml
# #script that defines the parameters, anchors, and each layer
# # parameters
# nc: {num_classes}  # number of classes
# depth_multiple: 0.33  # model depth multiple
# width_multiple: 0.50  # layer channel multiple
# 
# # anchors
# anchors:
#   - [10,13, 16,30, 33,23]  # P3/8
#   - [30,61, 62,45, 59,119]  # P4/16
#   - [116,90, 156,198, 373,326]  # P5/32
# 
# # YOLOv5 backbone
# backbone:
#   # [from, number, module, args]
#   [[-1, 1, Focus, [64, 3]],  # 0-P1/2
#    [-1, 1, Conv, [128, 3, 2]],  # 1-P2/4
#    [-1, 3, BottleneckCSP, [128]],
#    [-1, 1, Conv, [256, 3, 2]],  # 3-P3/8
#    [-1, 9, BottleneckCSP, [256]],
#    [-1, 1, Conv, [512, 3, 2]],  # 5-P4/16
#    [-1, 9, BottleneckCSP, [512]],
#    [-1, 1, Conv, [1024, 3, 2]],  # 7-P5/32
#    [-1, 1, SPP, [1024, [5, 9, 13]]],
#    [-1, 3, BottleneckCSP, [1024, False]],  # 9
#   ]
# 
# # YOLOv5 head
# head:
#   [[-1, 1, Conv, [512, 1, 1]],
#    [-1, 1, nn.Upsample, [None, 2, 'nearest']],
#    [[-1, 6], 1, Concat, [1]],  # cat backbone P4
#    [-1, 3, BottleneckCSP, [512, False]],  # 13
# 
#    [-1, 1, Conv, [256, 1, 1]],
#    [-1, 1, nn.Upsample, [None, 2, 'nearest']],
#    [[-1, 4], 1, Concat, [1]],  # cat backbone P3
#    [-1, 3, BottleneckCSP, [256, False]],  # 17 (P3/8-small)
# 
#    [-1, 1, Conv, [256, 3, 2]],
#    [[-1, 14], 1, Concat, [1]],  # cat head P4
#    [-1, 3, BottleneckCSP, [512, False]],  # 20 (P4/16-medium)
# 
#    [-1, 1, Conv, [512, 3, 2]],
#    [[-1, 10], 1, Concat, [1]],  # cat head P5
#    [-1, 3, BottleneckCSP, [1024, False]],  # 23 (P5/32-large)
# 
#    [[17, 20, 23], 1, Detect, [nc, anchors]],  # Detect(P3, P4, P5)
#   ]

# Commented out IPython magic to ensure Python compatibility.
# Weights & Biases
# %pip install -q wandb
import wandb
wandb.login()

# Commented out IPython magic to ensure Python compatibility.
# # train yolov5s on custom data for 1000 epochs
# # time its performance
# #training SAR YOLOv5 detector
# #epochs: define the number of training epochs. (Note: often, 3000+ are common here!)
# #data: set the path to our yaml file
# #cfg: specify our model configuration
# #weights: specify a custom path to weights. (Note: you can download weights from the Ultralytics Google Drive folder)
# #cache: cache images for faster training
# #name: result names
# %%time
# %cd /content/yolov5/
# 
# #img: define input image size
# #batch: determine batch size
# !python train.py --img 416 --batch 16 --epochs 1000 --data {dataset.location}/data.yaml --cfg ./models/custom_yolov5s.yaml --weights '' --name yolov5s_results  --cache
#

"""# Evaluate SAR Data Set YOLOv5 Detector Performance"""

# Commented out IPython magic to ensure Python compatibility.
# Start tensorboard
# Launch after you have started training
# logs save in the folder "runs"
#Evaluate YOLOv5 performance
# %load_ext tensorboard
# %tensorboard --logdir runs
#Training losses and performance metrics

# we can also output some older school graphs if the tensor board isn't working for whatever reason...

from utils.plots import plot_results  # plot results.txt as results.png
Image(filename='/content/yolov5/runs/train/yolov5s_results/results.png', width=1000)  # view results.png

# first, display our ground truth data
#Visualize YOLOv5 training data

print("GROUND TRUTH TRAINING DATA:")
Image(filename='/content/yolov5/runs/train/yolov5s_results/test_batch0_labels.jpg', width=900)

# print out an augmented training example
print("GROUND TRUTH AUGMENTED TRAINING DATA:")
Image(filename='/content/yolov5/runs/train/yolov5s_results/train_batch0.jpg', width=900)

# Commented out IPython magic to ensure Python compatibility.
# trained weights are saved by default in our weights folder
#YOLOv5 inference on test images

# %ls runs/

# Commented out IPython magic to ensure Python compatibility.
# %ls runs/train/yolov5s_results/weights

# Commented out IPython magic to ensure Python compatibility.
# when we ran this, we saw .007 second inference time. That is 140 FPS on a TESLA P100!
# use the best weights!

# %cd /content/yolov5/
!python detect.py --weights runs/train/yolov5s_results/weights/best.pt --img 416 --conf 0.4 --source ../test/images

#display inference on ALL test images
#this looks much better with longer training above

import glob
from IPython.display import Image, display

for imageName in glob.glob('/content/yolov5/runs/detect/exp2/*.jpg'): #assuming JPG
    display(Image(filename=imageName))
    print("\n")

from google.colab import drive
drive.mount('/content/gdrive')

# Commented out IPython magic to ensure Python compatibility.
# %cp /content/yolov5/runs/train/yolov5s_results/weights/best.pt /content/gdrive/My\ Drive
#Export saved YOLOv5 weights for future inference