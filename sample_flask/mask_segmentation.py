import albumentations
from albumentations.pytorch import ToTensorV2
from typing import List
import torch
import numpy as np
import albumentations as A
import torchvision.transforms as T
import segmentation_models_pytorch as smp
import os
import torchvision.transforms.functional as F
from torch.utils.data import Dataset, DataLoader
from matplotlib import colors, pyplot as plt
from PIL import Image
import warnings
warnings.filterwarnings("ignore")
from skimage.filters import threshold_otsu
from torchvision.utils import draw_segmentation_masks
from tqdm import tqdm

best_model = torch.load('static/model/nail_foot_seg_best_model.pth', map_location=torch.device('cpu'))

class test_NailsDataset(torch.utils.data.Dataset):
    def __init__(self, images: List[str], transform):
        self._images = images
        # self._masks = masks
        self._transform = transform
        # assert len(images) == len(masks)

    def __len__(self):
        return len(self._images)

    def __getitem__(self, index):
        image = Image.open(self._images[index])
        augmented = self._transform(image=np.array(image))
        image = augmented['image']
        return image

def test_dataset(test_image, img_name):
    test_dataset = test_NailsDataset(
        images=test_image,
        transform=A.Compose([
            A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            A.Resize(height=224, width=224),  # 사이즈 변경하면 오류
            A.Sharpen(p=0.5),
            ToTensorV2(transpose_mask=True),
        ]),
    )
    
    test_dataloader = torch.utils.data.DataLoader(test_dataset, batch_size=1, shuffle=False)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    iou_score, iou_score2, mean_acc, otsu = 0, 0, 0, 0
    for i, imgs in tqdm(enumerate(test_dataloader)):
        for img in imgs:
            img = torch.unsqueeze(img, 0)  # torch.unsqueeze(): 1차원 제거 함수
            pred = best_model((img).to(device))[0][0].cpu().detach().numpy() > 0.47
            
            # 시각화
            fig, axes = plt.subplots(1, 2)
            axes[0].imshow(pred)
            axes[0].set_title("Predicted mask")
            
            img_o = ((img).to(device))[0][0].cpu().detach().numpy()
            axes[1].imshow(img_o)
            axes[1].set_title("Target image")
            
            fig.set_figwidth(12)
            fig.set_figheight(6)
            

            # 마스크 이미지 저장
            plt.imsave(f'static/adain/hand_mask/model_mask_{img_name}', pred, cmap='gray')  # 경로 변경
            