import json
import requests
import os
import random
import time

import jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS

comment_file_path = 'test1.txt'
WC_MASK_IMG = "ej1.jpg"
WC_FONT_PATH = 'Library/Fonts/Songti.ttc'
sw = set(STOPWORDS)

def spider_ej(page=0):
    """爬取京东耳机商品评价"""
    url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1305&productId=7611546&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&fold=1' % page
    kv = {'user-agent': 'Mozilla/5.0', 'Referer': "https://item.jd.com/7611546.html"}
    try:
        r = requests.get(url, headers=kv)       # 有时候请求错误也会有返回数据
        # raise_for_status会判断返回状态码，如果4XX或5XX则会抛出异常
        r.raise_for_status()

    except:
        print('爬取失败')
    # 获得json数据字符串，截取
    r_json_str = r.text[26:-2]
    # 字符串转成对象
    r_json_obj = json.loads(r_json_str)
    # 获取评价列表数据，comments
    r_json_comment = r_json_obj['comments']
    # 遍历对象
    #for r_json_comment in r_json_comment:
        # 获取内容
        #print(r_json_comment['content'])
    # 遍历评论对象列表,comments里分列了，有许多列content，每一列就是一个用户的评论
    for r_json_comment in r_json_comment:
        # 以追加模式换行写入
        with open(comment_file_path, 'a+') as file:
            file.write(r_json_comment['content'] + '\n')
            # 打印评论内容
        print(r_json_comment['content'])
def batch_spider_comment():
    """批量爬取"""
    if os.path.exists(comment_file_path):
        os.remove(comment_file_path)
    for i in range(100):
        spider_ej(i)
        time.sleep(random.random() * 5)

def cut_word():
    """分词"""
    with open(comment_file_path) as file:
        comment_txt = file.read()
        wordlist = jieba.cut(comment_txt, cut_all=True)
        wl = " ".join(wordlist)
        sw.add("但是")
        sw.add("很")
        sw.add("我")
        sw.add("终于")
        print(wl)
        return wl

def create_wordcloud():
    """生成词云"""
    wc_mask = np.array(Image.open(WC_MASK_IMG))
    wc = WordCloud(background_color="white", stopwords=sw, max_words=500, mask=wc_mask, scale=4, max_font_size=50, random_state=20,
                   font_path=WC_FONT_PATH)
    wc.generate(cut_word())

    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.figure()
    plt.show()


if __name__ == '__main__':
    create_wordcloud()
