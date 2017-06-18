import re
import requests
from bs4 import BeautifulSoup as bs
import os


def getAv():
    av = input("请输入Av号:")
    url = "http://www.bilibili.com/video/av" + str(av) + "/"
    print("\n找到了url!")
    getHTMLText(url, av)


def getHTMLText(url, av):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)", }
    u = requests.get(url=url, headers=headers)
    html = u.text
    cid = re.findall(r'cid=(.*?)&aid=', html)[0]
    print("找到了弹幕cid!")
    getDanmu(cid, av)


def getDanmu(cid, av):
    dmurl = "http://comment.bilibili.com/" + str(cid) + ".xml"
    dmhtml = requests.get(dmurl).text
    ids = re.findall(r',0,(\w*?),\d*?">', dmhtml)
    print(ids)
    soup = bs(dmhtml, 'xml')
    dmlist = soup.find_all('d')
    print("装填弹幕内容!")
    printDanmu(dmlist, av, getName(findTrueid(ids)))


def findTrueid(ids):
    print("\n正在解开用户id的hash")
    api_start = "http://biliquery.typcn.com/api/user/hash/"
    trueidlist = []
    for id in ids:
        api = api_start + str(id)
        try:
            idhtml = requests.get(api)
            idtext = idhtml.text
            trueid = re.findall(r'"id":(.+?)}', idtext)[0]
            trueidlist.append(trueid)
            print("发现用户id:" + str(trueid))
        except:
            print("error")
            trueidlist.append("error")
            continue
    return trueidlist


def getName(trueidlist):
    namelist = []
    print("\n正在转化id为用户名")
    for i in trueidlist:
        url = "http://space.bilibili.com/" + str(i) + "/#!/"
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)", }
        r = requests.get(url=url, headers=headers)
        if r.status_code == 404:
            namelist.append("error")
            continue
        else:
            html = r.text
            soup = bs(html, "html.parser")
            Space = soup.find("h1", attrs={"class": "space-seo space-meta"})
            Name = re.sub("的个人空间。", "", Space.string)
            print("查询到用户名:" + Name)
            namelist.append(Name)
    return namelist


def printDanmu(dmlist, av, trueidlist):
    filename = "av" + str(av) + ".txt"
    print("\nLoad into " + str(filename) + "...\n")
    with open(filename, 'w', encoding='utf-8') as t:
        t.write("#Author:Lz1y   \n#blog:www.Lz1y.cn\n")
        t.write("error是因为发送者不是正式会员，或者被删号了")
        t.write("tip:弹幕发送者的空间:http://space.bilibili.com/数字id\n\n\n\n\n")
        for dm, id in zip(dmlist, trueidlist):
            t.write(str(id) + ':' + dm.string + '\n')
    print("Done!")


if __name__ == "__main__":
    getAv()