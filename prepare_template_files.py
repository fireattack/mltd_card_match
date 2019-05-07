import json

from requests import get  # to make GET request
from os.path import exists
import cv2
import numpy as np
from os import listdir

def downloadImg(url):
    filename = 'icons/' + url.split('/')[-1]
    if exists(filename):
        print(f'{filename} already exists.')
        return
    response = get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        print(f'Download error: {str(response.status_code)}')

with open("cards.json", "r", encoding='utf-8') as read_file:
    cards = json.load(read_file)

for card in cards:
    downloadImg(card['iconImg1'])
    downloadImg(card['iconImg2'])

# Crop icons.
files = [f for f in listdir('icons') if f.endswith('.png')]
for file in files:
    print(f'Processing {file}..')
    img = cv2.imread('icons/'+file)
    img = img[30:-34, 7:-10]
    if exists('icons_crop/' + file):
        print(f'Cropped version of {file} already exists.')
        continue
    cv2.imwrite('icons_crop/' + file, img)
    
from image_match.goldberg import ImageSignature


# Generate template signature matrix.
gis = ImageSignature()

files = [f for f in listdir('icons_crop') if f.endswith('.png')]
for file in files:
    print(f'Processing {file}..')
    if exists(f'sigs/{file}.npy'):
        print(f'Signature of {file} already exists.')
        continue
    sig = gis.generate_signature('icons_crop/' + file)    
    np.save(f'sigs/{file}.npy', sig)