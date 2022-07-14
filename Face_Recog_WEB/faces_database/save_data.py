import pickle
import os
from torchvision import transforms
import torch
from PIL import Image
# from insightface.insight_face import iresnet100
import numpy as np

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# # model_emb = insight_face(path="insightface/ckpt_epoch_50.pth", device=device, train=True)
# weight = torch.load("./insightface/16_backbone.pth", map_location = device)
# model_emb = iresnet100()
# model_emb.load_state_dict(weight)
# model_emb.to(device)
# model_emb.eval()

# face_preprocess = transforms.Compose([
#                                     transforms.ToTensor(), # input PIL => (3,56,56), /255.0
#                                     transforms.Resize((112, 112)),
#                                     transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
#                                     ])

# def inference_database(root_path = "faces_database"):
    
#     images_name = []
#     images_emb = []
    
#     for folder in os.listdir(root_path):
#         if os.path.isdir(root_path + "/"+ folder):
#             for name in os.listdir(root_path + "/" + folder):
#                 if name.endswith(("png", 'jpg', 'jpeg')):
#                     path = f"{root_path}/{folder}/{name}"
                    
#                     img_face = face_preprocess(Image.open(path).convert("RGB")).to(device)

#                     with torch.no_grad():
#                         emb_img_face = model_emb(img_face[None, :])[0].cpu().numpy()
                    
#                     images_emb.append(emb_img_face)
#                     images_name.append(name.split('.')[0])

#     images_emb = np.array(images_emb)
#     images_name = np.array(images_name)
    
#     return images_name, images_emb/np.linalg.norm(images_emb, axis=1, keepdims=True)

# name_images, emb_images = inference_database("faces_database")

file = open('./faces_database/data.pickle','rb')
db = pickle.load(file)
name_images1 = np.array(list(db.keys()))
emb_images1 = np.array(list(db.values()))
print("=================================================")
for item in db.items():
    print(item)
    print("==============================================================================================")
