from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES
from os import listdir
from os.path import join
import json
from mltd_card_match import getBestMatchWithImageSignature
import time

import concurrent.futures

    

es = Elasticsearch()
ses = SignatureES(es)

# files = [f for f in listdir('icons_crop') if f.endswith('.png')]
# for file in files:
#     ses.delete_duplicates(join('icons_crop', file))


# result = ses.search_image('cropped_samples/00.png')[0]["path"]
# print(result)

def search(card):
    result = ses.search_image(card)[0]["path"]
    print(result)

start_time = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
    for cardToMatch in listdir('cropped_samples'):
        card = join('cropped_samples', cardToMatch)
        ex.submit(search, card)

elapsed_time1 = time.time() - start_time
print(f'Using DB: elapsed time = {elapsed_time1:.2f}s')
