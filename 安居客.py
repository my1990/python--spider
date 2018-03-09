import requests,re
from bs4 import BeautifulSoup

Baseurl = 'https://hz.fang.anjuke.com/loupan/all/p'
area_re = re.compile(r'<span>建筑面积：(.*?)</span>')
id = 1
while True:
    url = Baseurl + str(id) + '/'
    requests_session = requests.Session()
    data = requests_session.get(url).text
    soup = BeautifulSoup(data,'html.parser')

    item_list = soup.find_all(attrs=["item-mod"])
    for item in item_list:
        if item.h3:
            name = item.h3.a.string                            #小区名
            address = item.find(attrs="address").a.string     #小区位置
            if item.find(attrs="price"):
                price = item.find(attrs="price").span.string  #小区价格
            else:
                price = "售价待定"
            if area_re.findall(str(item)):
                area = area_re.findall(str(item))[0]
            else:
                area = "尚未公开"
            print("小区名：%s \n小区位置：%s \n小区价格：%s \n房间面积：%s" % (name,address,price,area) )
            print("\n")

    href_re = re.compile(r'<a href="(.*?)" class="next-page next-link">下一页</a>')
    if href_re.findall(data):
        print("第%s页" % id)
        id += 1
    else:
        print("全部爬完，共%s页" % id)
        break
