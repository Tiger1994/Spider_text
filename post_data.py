# -*- coding:utf-8 -*-
import requests
import os
import time
import json
import datetime
import tqdm

if __name__ == '__main__':
    dataset_path = './dataset'
    url = 'http://182.92.218.30:1984/resource'
    for name in tqdm.tqdm(os.listdir(dataset_path)):
        file_path = dataset_path+'/'+name
        with open(file_path, 'r', encoding='UTF-8') as data_f:
            json_data = json.load(data_f)
        json_data['time'] = datetime.datetime.now().strftime('%Y-%m-%d')
        data = json.dumps(json_data, ensure_ascii=False)
        res = requests.post(url, data=data.encode())

        time.sleep(5)
