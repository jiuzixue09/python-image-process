from enum import Enum

import cv2 as cv
from PIL import Image


class Detector(Enum):
    FAST = 1
    STAR = 2


class BriefFeature:
    def __init__(self, fast_threshold=10, detector=Detector.FAST):
        # Initiate Star detector
        self.star = cv.xfeatures2d.StarDetector_create()
        # Initiate FAST detector
        self.fast = cv.FastFeatureDetector_create(fast_threshold)
        # Initiate BRIEF extractor
        self.brief = cv.xfeatures2d.BriefDescriptorExtractor_create()

        self.detector = self.get_fast_feature if detector == Detector.FAST else self.get_brief_feature

    def get_fast_feature(self, img):
        # find the keypoints with FAST
        kp = self.fast.detect(img, None)
        # compute the descriptors with BRIEF
        kp, des = self.brief.compute(img, kp)
        return kp, des

    def get_brief_feature(self, img):
        # find the keypoints with STAR
        kp = self.star.detect(img, None)
        # compute the descriptors with BRIEF
        kp, des = self.brief.compute(img, kp)
        return kp, des

    @staticmethod
    def read_file(img1, img2):
        img1 = cv.imread(img1, 0)
        img2 = cv.imread(img2, 0)
        img1 = cv.resize(img1, (200, 200))
        img2 = cv.resize(img2, (200, 200))
        if img1 is None or img2 is None:
            raise ValueError('image read error!!!')

        return img1, img2

    def score(self, img1, img2, max_distance=None, matches_point=None, save_path=None):
        img1, img2 = self.read_file(img1, img2)

        kp1, des1 = self.detector(img1)
        kp2, des2 = self.detector(img2)

        # create BFMatcher object
        bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
        # Match descriptors.
        matches = bf.match(des1, des2)
        if max_distance is not None:
            matches = [m for m in matches if m.distance <= max_distance]

        if save_path is not None:
            if matches_point is None:
                matches_point = min(len(kp1), len(kp2))

            img3 = cv.drawMatches(img1, kp1, img2, kp2, matches[:matches_point], None,
                                  flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            Image.fromarray(img3).save(save_path)

        l1, l2 = len(kp1), len(kp2)
        confidence = l1 / l2 if l1 < l2 else l2 / l1

        return confidence, len(matches) / min(l1, l2)

    def match(self, img1, img2, max_distance=10):
        img1, img2 = self.read_file(img1, img2)

        kp1, des1 = self.detector(img1)
        kp2, des2 = self.detector(img2)

        # create BFMatcher object
        bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
        # Match descriptors.
        matches = bf.match(des1, des2)
        # Sort them in the order of their distance.
        matches = sorted((m for m in matches if m.distance <= max_distance), key=lambda x: x.distance)
        return matches

    def match_and_show(self, img1, img2, matches_point=None, max_distance=10):
        img1, img2 = self.read_file(img1, img2)

        from matplotlib import pyplot as plt
        kp1, des1 = self.detector(img1)
        kp2, des2 = self.detector(img2)

        # create BFMatcher object
        bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
        # Match descriptors.
        matches = bf.match(des1, des2)
        # Sort them in the order of their distance.
        matches = sorted((m for m in matches if m.distance <= max_distance), key=lambda x: x.distance)
        if matches_point is None:
            matches_point = min(len(kp1), len(kp2))
        # Draw first 30 matches.
        img3 = cv.drawMatches(img1, kp1, img2, kp2, matches[:matches_point], None,
                              flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        plt.imshow(img3), plt.show()
