# from PIL import Image
# import torchvision.transforms as transforms
# import torchvision.models as models
# import torch
# import json
# import requests
# import os
#
# def load_and_transform_image(image_path, target_size=(224, 224)):
#     image = Image.open(image_path).convert('RGB')
#     transform = transforms.Compose([
#         transforms.Resize(target_size),
#         transforms.ToTensor(),
#         transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
#     ])
#     image = transform(image).unsqueeze(0)
#     return image
#
# def recognize_image(image_path):
#     processed_image = load_and_transform_image(image_path)
#     model = models.resnet50(pretrained=True)
#     model.eval()
#
#     with torch.no_grad():
#         outputs = model(processed_image)
#         probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
#
#     # Get ImageNet class index to name mapping
#     imagenet_class_index_url = 'https://storage.googleapis.com/download.tensorflow.org/data/imagenet_class_index.json'
#     class_idx = requests.get(imagenet_class_index_url).json()
#
#     def idx_to_class(index):
#         return class_idx[str(index)][1]
#
#     # 获取当前文件的目录
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#
#     # 加载中文类别映射
#     with open(os.path.join(dir_path, 'imagenet_classes_cn.json'), 'r', encoding='utf-8') as f:
#         class_idx_cn = json.load(f)
#
#     def idx_to_class_cn(index):
#         return class_idx_cn[str(index)]
#
#     top3_probs, top3_classes = torch.topk(probabilities, 3)
#     results=[]
#
#     for i in range(top3_probs.size(0)):
#         class_id = top3_classes[i].item()
#         class_name_cn = idx_to_class_cn(class_id)
#         probability = top3_probs[i].item()
#         results.append((class_id, class_name_cn, probability))
#
#
#     return results