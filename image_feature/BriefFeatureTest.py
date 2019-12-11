import time

from image_feature.BriefFeature import BriefFeature, Detector

if __name__ == '__main__':
    b = BriefFeature(20, Detector.FAST)
    img1 = '/home/hdc/Pictures/test/jhk-1569048683183.jpg'
    img2 = '/home/hdc/Pictures/test/jhk-1569048683183-copy.jpg'
    start = time.time()
    score = b.score(img1, img2)
    print(time.time()-start)
    print(score)
    b.match_and_show(img1, img2)
