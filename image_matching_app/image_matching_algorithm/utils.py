import cv2
import kornia as K
import kornia.feature as KF
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import torch
from kornia_moons.viz import draw_LAF_matches
from datetime import datetime
from django.conf import settings

matplotlib.use('agg')
matcher = KF.LoFTR(pretrained=settings.PREDEFINED_MODEL)

images_size = (480, 640)

if settings.PREDEFINED_MODEL == "outdoor":
    images_size = (600, 375)


def preprocess_and_inference(fname1,fname2):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    img1 = K.io.load_image(fname1, K.io.ImageLoadType.RGB32)[None, ...]
    img2 = K.io.load_image(fname2, K.io.ImageLoadType.RGB32)[None, ...]

    img1 = K.geometry.resize(img1, images_size, antialias=True)
    img2 = K.geometry.resize(img2, images_size, antialias=True)

    input_dict = {
    "image0": K.color.rgb_to_grayscale(img1),  # LofTR works on grayscale images only
    "image1": K.color.rgb_to_grayscale(img2),
    }

    with torch.inference_mode():
        correspondences = matcher(input_dict)

    mkpts0 = correspondences["keypoints0"].cpu().numpy()
    mkpts1 = correspondences["keypoints1"].cpu().numpy()
    Fm, inliers = cv2.findFundamentalMat(mkpts0, mkpts1, cv2.USAC_MAGSAC, 1.0, 0.999, 100000)
    inliers = inliers > 0

    draw_LAF_matches(
        KF.laf_from_center_scale_ori(
            torch.from_numpy(mkpts0).view(1, -1, 2),
            torch.ones(mkpts0.shape[0]).view(1, -1, 1, 1),
            torch.ones(mkpts0.shape[0]).view(1, -1, 1),
        ),
        KF.laf_from_center_scale_ori(
            torch.from_numpy(mkpts1).view(1, -1, 2),
            torch.ones(mkpts1.shape[0]).view(1, -1, 1, 1),
            torch.ones(mkpts1.shape[0]).view(1, -1, 1),
        ),
        torch.arange(mkpts0.shape[0]).view(-1, 1).repeat(1, 2),
        K.tensor_to_image(img1),
        K.tensor_to_image(img2),
        inliers,
        draw_dict={
            "inlier_color": (0.1, 1, 0.2),
            "tentative_color": None,
            "feature_color": (0.1, 0.5, 1),
            "vertical": False,
        },
        ax=ax,
    )
    now = datetime.now() 
    output_filename = now.strftime("%m%d%Y%H%M%S")
    plt.savefig(f'media/{output_filename}.png')

    return f'{output_filename}.png'
