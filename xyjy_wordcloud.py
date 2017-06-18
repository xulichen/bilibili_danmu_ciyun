import requests
import re
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import jieba
import os
import nltk
from scipy.misc import imread
import matplotlib.pyplot as plt

d = os.path.dirname('.')


def get_comments():
    """
    找到你在bilibili视频网站上所看视频的av号
    我选择了新垣结衣的一个视频链接
    """
    url = 'https://www.bilibili.com/video/av2783167/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    html = requests.get(url=url, headers=headers)
    source = html.text
    cid = re.findall('cid=(.*?)&aid', source)[0]
    danmu_url = 'http://comment.bilibili.com/{}.xml'.format(cid)
    danmu_html = requests.get(url=danmu_url, headers=headers)
    danmu_source = danmu_html.text
    comments = re.findall('">(.*?)</d>', danmu_source)
    with open('xyjy-t.txt', 'w') as f:
        for comment in comments:
            f.writelines(comment + ' ')


def comments_analyse():
    with open('xyjy-t.txt', 'r') as f:
        all_word = f.read()

    all_word = re.sub('\？|，|。', '', all_word)
    seg = jieba.cut(sentence=all_word)
    segList = []
    for i in seg:
        segList.append((i))

    # 打印字符串
    print(all_word)

    lis = all_word.split(' ')

    freq = nltk.FreqDist(lis)

    print(freq)
    # keys = freq.keys()
    items = freq.items()
    # 构造字词: 字词的出现次数的字典
    dicts = dict(items)
    # 根据出现次数进行排序
    sort_dicts = sorted(dicts.items(), key=lambda d: d[1], reverse=True)
    # 打印字典
    print(dicts)
    # 打印逆序列表
    print(sort_dicts)

    # 加载中文字体
    font = os.path.join(d, 'DroidSansFallback.ttf')
    # 背景图片
    back_color = imread(os.path.join(d, 'timg.jpeg'))

    wc = WordCloud(background_color="white",
                   max_words=2000,
                   mask=back_color,
                   font_path=font,
                   stopwords=STOPWORDS.add("said"),
                   max_font_size=40,
                   random_state=50)

    # 可多次尝试wc.generate()及generate_from_frequencies(),并选择对应的字符串及字典构造
    wc.generate(all_word)

    image_color = ImageColorGenerator(back_color)

    # plt.imshow(wc)
    plt.figure()
    plt.imshow(wc.recolor(color_func=image_color))
    plt.axis("off")
    plt.show()

    wc.to_file(os.path.join(d, '新垣结衣.jpg'))

if __name__ == '__main__':
    get_comments()
    comments_analyse()
