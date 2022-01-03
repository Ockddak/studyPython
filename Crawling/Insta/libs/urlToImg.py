# 이미지 다운로드/도식화를 위한 라이브러리 가져오기
import matplotlib.pyplot as plt
import tempfile
from six.moves.urllib.request import urlopen
from six import BytesIO

# 이미지 상에 그리기 모듈 가져오기
import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

# csv데이터 불러오기
import pandas as pd

def display_image(image):
    fig = plt.figure(figsize=(20, 15))
    plt.grid(False)
    plt.imshow(image)

def download_and_resize_image(url, save_path, new_width=256, new_height=256,
                              display=False):
    response = urlopen(url)
    image_data = response.read()
    image_data = BytesIO(image_data)

    pil_image = Image.open(image_data)
    pil_image = ImageOps.fit(pil_image, (new_width, new_height), Image.ANTIALIAS)
    pil_image_rgb = pil_image.convert("RGB")
    pil_image_rgb.save(save_path, format="JPEG", quality=90)
    print("Image downloaded to %s." % save_path)
    if display:
        display_image(pil_image)
    return save_path


