import cv2
import numpy as np
from os import listdir, makedirs
from os.path import join, exists
import argparse
from image_match.goldberg import ImageSignature
import json
from shutil import rmtree
import time

gis = ImageSignature()


def getBestMatchWithImageSignature(card, sigs='sigs'):
    a = gis.generate_signature(card)
    files = [f for f in listdir(sigs) if f.endswith('.npy')]
    for file in files:
        b = np.load(join(sigs, file))
        score = gis.normalized_distance(a, b)
        if score <= 0.45:
            bestMatch = file.replace('.npy', '')
            break

    print(f'{card}\'s best match: {bestMatch}')
    return bestMatch


def getBestMatchWithTemplateMatching(card, templates='icons_crop'):
    img = cv2.imread(card, 0)
    scores = []
    files = [f for f in listdir(templates) if f.endswith('.png')]
    for file in files:
        template = cv2.imread(join(templates, file), 0)
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        scores.append((file, max_val))

    scores = sorted(scores, key=lambda score: score[1], reverse=True)
    bestMatch = scores[0][0]
    bestScore = scores[0][1]
    secondBest = scores[1][1]
    print(f'{bestScore}, {secondBest}')
    print(f'{card}s best match: {bestMatch}')
    return bestMatch


def card_cut(img_path, save_folder):  # Separate cards from screenshots

    img_orig = cv2.imread(img_path)
    h, w, c = img_orig.shape
    new_w = round(887 / h * w)
    w_offset = round((new_w-1173)/2)
    img_orig = cv2.resize(img_orig, (new_w, 887),
                          interpolation=cv2.INTER_CUBIC)
    img_orig = img_orig[105:-130, w_offset: - w_offset]
    img = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY)

    if not exists(save_folder):
        makedirs(save_folder)

    m = np.mean(img, axis=1)

    cols = []

    j = 0
    j_last = -1
    for i in np.nditer(m):
        if i > 215:
            if j - j_last >= 120:  # high enough
                cols.append((j_last+1, j-1))
            j_last = j
            img[j, :] = 0
        j = j + 1

    x = 0
    for (y1, y2) in cols:
        for i in range(0, 8):
            crop = img_orig[y1 + 22:y2 - 30, 46 + 138 * i:159 + 138 * i, :]
            print(f'Saving {x:02}.png..')
            cv2.imwrite(join(save_folder, f'{x:02}.png'), crop)
            x = x + 1


def card_match(path, remove_temp_file=True):

    tempName = str(time.time())
    card_cut(path, tempName)

    # Load card metadata
    with open("cards.json", "r", encoding='utf-8') as read_file:
        cards = json.load(read_file)

    # Prepare report HTML file
    html = """<!DOCTYPE html>
    <html>

    <head>
        <style>
            .grid-container {
                display: grid;
                grid-template-columns: 10vw 10vw 10vw 10vw 10vw 10vw 10vw 10vw;
                justify-content:center;
            }

            .grid-item {
                font-size: 16px;            
                text-align: center;
                overflow: hidden;
            }

            img {
                width: 10vw;
                max-width: 150px;
            }
        </style>
    </head>
    <body><div class="grid-container">
    """

    # Matching each card we got from screenshots
    for cardToMatch in listdir(tempName):
        card = join(tempName, cardToMatch)
        bestMatch = getBestMatchWithImageSignature(card)
        for card in cards:
            if bestMatch in card['iconImg1'] or bestMatch in card['iconImg2']:
                html = html + \
                    f'<div class="grid-item"> <a href="https://mltd.matsurihi.me/cards/{card["cardID"]}"><img src="icons/{bestMatch}""></a><p>{card["cardName"].replace("　","<br />")}</div>\n'
#                   f'<div class="grid-item"> <a href="https://mltd.matsurihi.me/cards/{card["cardID"]}"><img src="icons/{bestMatch.replace(".png",".jpg")}"></a><p>{card["cardName"].replace("　","<br />")}</div>\n'
                break

    html = html + '</div> </body> </html>'
    if not exists('report'):
        makedirs('report')
    htmlFileName = join('report', f'{tempName}.html')
    with open(htmlFileName, "w", encoding='utf-8') as htmlFile:
        htmlFile.write(html)
    if remove_temp_file:
        rmtree(tempName)
    return f'{tempName}.html'


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("screenshot_file", nargs='?', default='img.jpg')
    args = parser.parse_args()
    path = args.screenshot_file

    card_match(path)
