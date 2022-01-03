#!/usr/bin/env python
# coding: utf-8

# In[26]:


from PIL import Image
from PIL.ExifTags import TAGS
import cv2
import os
import json
import numpy as np
import matplotlib.pyplot as plt

jsonPath = '../files/orange_notAcq_json/notAcq/'
imgPath  = '../files/orange_notAcq_jpg/notAcq/'
maskingPath = imgPath.replace('notAcq/', 'masking/')
jsonList = os.listdir(jsonPath)

for j in jsonList :
    imgFile  = imgPath + j.replace('.json', '') + '.jpg'
    
    
    with open(jsonPath + j, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
#     print(json_data)
    x_list, y_list = json_data['Annotations']['BNDBX'].split(',')
    x_list = map(int, x_list[1:-1].split('|'))
    y_list = map(int, y_list[1:-1].split('|'))

    poly_ary = []
    for i in zip(x_list, y_list) :
        poly_ary.append(i)
    pt1 = np.array(poly_ary, np.int32)
    
    img  = cv2.imread(imgFile)
    h, w, c = img.shape
    mask = np.zeros((h, w, c), np.uint8) + 255
    mask = cv2.fillPoly(mask, [pt1], (0, 0, 0))
    
    masked = cv2.bitwise_or(img, mask)
    
    save   = maskingPath + j.replace('.json', '') + '.jpg'
    cv2.imwrite(save, masked)
    print('%3s 완료.' %(j.replace('.json', '') + '.jpg'))


# In[22]:


imgFile  = imgPath + jsonList[0].replace('.json', '') + '.jpg'



with open(jsonPath + jsonList[0], 'r', encoding='utf-8') as f:
    json_data = json.load(f)
x_list, y_list = json_data['Annotations']['BNDBX'].split(',')
# print(y_list)
x_list = map(int, x_list[1:-1].split('|'))
y_list = map(int, y_list[1:-1].split('|'))

poly_ary = []
for i in zip(x_list, y_list) :
    poly_ary.append(i)

    
pt1 = np.array(poly_ary, np.int32)
# poly_ary
img  = cv2.imread(imgFile)

mask = np.zeros((1080, 1920, 3), np.uint8) + 255
# mask = cv2.fillConvexPoly(mask, pt1, (255, 255, 255))
mask = cv2.fillPoly(mask, [pt1], (0, 0, 0))
# polyline = cv2.polylines(mask, [pt1], True, (0, 255, 0), 2)  #닫힌 도형
# imgFile

# white_mask = np.zeros((1080, 1920, 3), np.uint8) + 255
test = cv2.bitwise_or(img, mask)
# cv2.imshow('line', polyline)
# cv2.imshow('mask', mask)
cv2.imshow('test',img)
cv2.imshow('masked', test)
cv2.waitKey(0)
cv2.destroyAllWindows()


# In[11]:


# meta_data = img._getexif()

# meta_data
exif = {}
for tag, value in img._getexif().items():

#extarcting all the metadata as key and value pairs and converting them from numerical value to string values
    if tag in TAGS:
        exif[TAGS[tag]] = value

#checking if image is copyrighted      
try:
    if 'Copyright' in exif:
        print("Image is Copyrighted, by ", exif['Copyright'])
except KeyError:
    pass

print()
print("Displaying all the metadatas of the image: \n")
print(exif)

