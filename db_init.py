from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES
from os import listdir
from os.path import join
import json
from mltd_card_match import getBestMatchWithImageSignature
import time

es = Elasticsearch()
ses = SignatureES(es)

files = [f for f in listdir('icons_crop') if f.endswith('.png')]
for file in files:
    ses.add_image(join('icons_crop', file))

start_time = time.time()

for cardToMatch in listdir('cropped_samples'):
    card = join('cropped_samples', cardToMatch)
    result = ses.search_image(card)[0]["path"]
    print(result)

elapsed_time1 = time.time() - start_time

start_time = time.time()

for cardToMatch in listdir('cropped_samples'):
    card = join('cropped_samples', cardToMatch)
    result = getBestMatchWithImageSignature(card)
    print(result)
elapsed_time2 = time.time() - start_time

print(f'Using DB: elapsed time = {elapsed_time1:.2f}s')
print(f'No DB: elapsed time = {elapsed_time2:.2f}s')