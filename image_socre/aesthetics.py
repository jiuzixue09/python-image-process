import torch
import torchvision.transforms as trns
from PIL import Image
import gc

# python3 -m pip install --upgrade torch torchvision -i https://pypi.tuna.tsinghua.edu.cn/simple
from memory_profiler import profile


class Aesthetics:

    def __init__(self):
        self.model = torch.jit.load("/home/hdc/Downloads/flickr_score_model.jit")
        torch.set_num_threads(4)
        self.MAX_EDGE = 800
        self.transform = trns.Compose([trns.ToTensor(), trns.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])
        print('init')

    def load_img(self, file):
        if isinstance(file, Image.Image):
            img = file
        else:
            img = Image.open(file)

        img = img.convert("RGB")
        w, h = img.size
        max_e = max(w, h)
        if max_e > self.MAX_EDGE:
            coe = self.MAX_EDGE / max_e
            img = img.resize([int(w * coe), int(h * coe)], 3)
        return img

    @profile
    def aesthetic_score(self, file):
        with self.load_img(file) as img:
            img_arr = self.transform(img).unsqueeze(0)  # .to(device)
            with torch.no_grad():
                item = self.model(img_arr).item()
                gc.collect()
                return item


aesthetic = Aesthetics()
print(aesthetic.aesthetic_score('/home/hdc/Downloads/9db1243c12c36a94920565facca927d6.jpg'))
