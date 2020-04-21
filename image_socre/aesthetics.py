import torch
import torchvision.transforms as trns
from PIL import Image

# python3 -m pip install --upgrade torch torchvision -i https://pypi.tuna.tsinghua.edu.cn/simple
model = torch.jit.load("/home/hdc/Downloads/flickr_score_model.jit")
transform = trns.Compose([trns.ToTensor(), trns.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])
torch.set_num_threads(4)

MAX_EDGE = 800


def load_img(file):
    if isinstance(file, Image.Image):
        img = file
    else:
        img = Image.open(file)

    img = img.convert("RGB")
    w, h = img.size
    max_e = max(w, h)
    if max_e > MAX_EDGE:
        coe = MAX_EDGE / max_e
        img = img.resize([int(w * coe), int(h * coe)], 3)
    return img


def flickr_score(file):

    img = load_img(file)
    img_arr = transform(img).unsqueeze(0)  # .to(device)
    with torch.no_grad():
        return model(img_arr)

