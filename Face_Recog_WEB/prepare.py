import torch
from PIL import Image
from torchvision import transforms
import torchvision
# other lib
import sys
import numpy as np
import os
import pandas as pd
import cv2
import matplotlib.pyplot as plt
from PIL import Image
# model_embedded_face (insightface)
from insightface.insight_face import iresnet100
import pickle

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
weight = torch.load("./insightface/16_backbone.pth", map_location=device)
model_emb = iresnet100()
model_emb.load_state_dict(weight)
model_emb.to(device)
model_emb.eval()

face_preprocess = transforms.Compose([
    transforms.ToTensor(),  # input PIL => (3,56,56), /255.0
    transforms.Resize((112, 112)),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

########################################################
# Đổ database đã lưu dô model để recog
file = open('./faces_database/data.pickle','rb')
db = pickle.load(file)
name_images = np.array(list(db.keys()))
emb_images = np.array(list(db.values()))

########################################################

sys.path.insert(0, "yolov5_face")

# from collections.abc import Iterable
from yolov5_face.models.experimental import attempt_load
from yolov5_face.utils.datasets import letterbox
from yolov5_face.utils.general import check_img_size, non_max_suppression_face, scale_coords
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = attempt_load("yolov5_face/yolov5s-face.pt", map_location=device)

########################################################
size_convert = 640  # setup size de day qua model
conf_thres = 0.4
iou_thres = 0.5
########################################################
#resize image
def resize_image(img0, img_size, orgimg):
    h0, w0 = orgimg.shape[:2]  # orig hw
    r = img_size / max(h0, w0)  # resize image to img_size
    if r != 1:  # always resize down, only resize up if training with augmentation
        interp = cv2.INTER_AREA if r < 1 else cv2.INTER_LINEAR
        img0 = cv2.resize(img0, (int(w0 * r), int(h0 * r)), interpolation=interp)

    imgsz = check_img_size(img_size, s=model.stride.max())  # check img_size
    img = letterbox(img0, new_shape=imgsz)[0]

    # Convert
    img = img[:, :, ::-1].transpose(2, 0, 1).copy()  # BGR to RGB, to 3x416x416

    img = torch.from_numpy(img).to(device)
    img = img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0

    return img