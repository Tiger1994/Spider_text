import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
import jieba
import datetime


def get_content(target):
    req = requests.get(url = target)
    req.encoding = 'utf-8'
    html = req.text
    bf = BeautifulSoup(html, 'lxml')
    texts = bf.find('div', id='content')
    content = texts.text.strip().split('\xa0'*4)
    return content


if __name__ == '__main__':
    server = 'https://www.xsbiquge.com'
    save_path = './dataset'
    target = 'https://www.xsbiquge.com/95_95052/'
    stopwords = [line.strip() for line in open("CS.txt", encoding="utf-8").readlines()]
    req = requests.get(url=target)
    req.encoding = 'utf-8'
    html = req.text
    chapter_bs = BeautifulSoup(html, 'lxml')
    chapters = chapter_bs.find('div', id='list')
    chapters = chapters.find_all('a')
    record = dict()
    record['author'] = "吴楚飞"
    record['time'] = datetime.datetime.now().strftime('%Y-%m-%d')
    for chapter in tqdm(chapters):
        chapter_name = chapter.string
        url = server + chapter.get('href')
        content = get_content(url)
        record['title'] = chapter_name
        content = ''.join(content)
        record['content'] = content
        words = jieba.lcut(content)
        counts = {}
        for word in words:
            if word not in stopwords:
                if len(word) == 1:
                    continue
                else:
                    counts[word] = counts.get(word, 0) + 1
        counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        keywords = ''
        keywords_len = min(5, len(counts))
        for i in range(keywords_len):
            keywords = keywords + counts[i][0] + ' '
        keywords = keywords.rstrip()
        record['keywords'] = keywords

        save_name = 'dataset/'+chapter_name+'.json'
        with open(save_name, "w", encoding='utf-8') as f:
            json.dump(record, f, indent=2, sort_keys=True, ensure_ascii=False)
