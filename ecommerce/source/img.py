import os
import torch
from torchvision import models, transforms
from torchvision.models.resnet import ResNet50_Weights
from PIL import Image
from torch.nn.functional import cosine_similarity
import logging

logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(asctime)s - %(message)s')

class ImageComparator:
    @classmethod
    def __init__(cls):
        cls.model = models.resnet50(weights=ResNet50_Weights.DEFAULT)
        cls.model = cls.model.eval()

        cls.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    @classmethod
    def extract_features(cls, img_path):
        img = Image.open(img_path).convert("RGB")
        img = cls.preprocess(img)
        img = img.unsqueeze(0)

        with torch.no_grad():
            features = cls.model(img)

        return features

    @classmethod
    async def compare(cls, img1_path, img2_path, threshold):
        try:
            if not os.path.exists(img1_path) or not os.path.exists(img2_path):
                return False

            img1_features = cls.extract_features(img1_path)
            img2_features = cls.extract_features(img2_path)

            similarity = cosine_similarity(img1_features, img2_features).item()
            # print(f'Similarity of two image: {similarity * 100:.2f}%')
            # print('img1_path:', img1_path)
            # print('img2_path:', img2_path)

            return similarity >= threshold
        except Exception as e:
            logging.error('Image compare error:', str(e))
            return False
