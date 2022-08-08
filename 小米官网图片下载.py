import requests
import aiohttp
import asyncio
import os
import re
from lxml import etree

# 下载图片
async def download(name, url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as picture:
            with open(name, mode='wb') as fp:
                fp.write(await picture.content.read())

# 异步下载主函数
async def downMain(name_list, url_list):
    tasks = []
    for num in range(0, len(name_list)):
        tasks.append(asyncio.create_task(download(name_list[num], url_list[num])))
    await asyncio.wait(tasks)

# 首页图片下载
def first_page():
    first_img_name_list = []
    first_img_url_list = []
    img = first_page_xpath.xpath('//*[@class="content"]/div/div/div/div[1]/div/div[2]/div/img[2]')
    for i in img:
        img_url = i.xpath('./@src')
        img_name = str(img_url[0]).split("?")[0].lstrip('https://img.youpin.mi-img.com/ferriswheel/')
        first_img_url_list.append(img_url[0])
        first_img_name_list.append('小米官网/' + img_name)
    loop.run_until_complete(downMain(first_img_name_list, first_img_url_list))

# 小米商城图片下载
def shop_page():
    shop_img_name_list = []
    shop_img_url_list = []
    shop_page_request = requests.get(url_list[1], headers=heard)
    shop_page_xpath = etree.HTML(shop_page_request.text)

    # 各种类的小图片
    try:
        os.mkdir('小米商城/小图片')
    except BaseException:
        pass
    small_xpath_li = shop_page_xpath.xpath('//*[@id="J_categoryList"]/li')
    for li in small_xpath_li:
        a = li.xpath('./div/ul/li/a')
        for img in a:
            img_url = img.xpath('./img/@data-src')
            img_name = img.xpath('./span/text()')
            shop_img_url_list.append(img_url[0])
            shop_img_name_list.append('小米商城/小图片/' + str(img_name[0]).replace("/", "&").rstrip("\"") + '.jpg')

    # 功能图标
    try:
        os.mkdir('小米商城/功能图标')
    except BaseException:
        pass
    icon_xpath_a = shop_page_xpath.xpath('//*[@id="app"]/div[2]/div/div[2]/div[1]/ul/li/a')
    for icon in icon_xpath_a:
        icon_url = icon.xpath('./img/@src')
        icon_name = icon.xpath('./img/@alt')
        shop_img_name_list.append('小米商城/功能图标/' + icon_name[0] + '.png')
        shop_img_url_list.append(icon_url[0])

    # 滚动大图
    try:
        os.mkdir('小米商城/滚动大图')
    except BaseException:
        pass
    big_xpath_a = shop_page_xpath.xpath('//*[@id="J_homeSwiper"]/div[1]/div/a')
    for big_img in big_xpath_a:
        big_url = big_img.xpath('./img/@key')
        big_name = str(big_url[0]).split('?')[0].lstrip('https://cdn.cnbj1.fds.api.mi-img.com/mi-mall/')
        shop_img_url_list.append(big_url[0])
        shop_img_name_list.append('小米商城/滚动大图/'+big_name)

    # 分类图片 图片链接在js中，但依然显示在源码里，换正则表达式筛选
    try:
        os.mkdir('小米商城/分类图片')
    except BaseException:
        pass
    try:
        os.mkdir('小米商城/分类图片/大图')
    except BaseException:
        pass
    sort_img_url_list = []
    sort_img_name_list = []
    pattern_big = re.compile(r'"img_url":"(?P<sort_big_img_url>https://cdn.cnbj1.fds.api.mi-img.com/mi-mall/\w*.\w{3}\?w=\d*)\\u0026h=')
    pattern = re.compile(r'"img_url":"(?P<sort_img_url>.{10,100})","product_id":.*?"product_name":"(?P<img_name>.*?)"', re.S)
    sort_big_img = pattern_big.finditer(shop_page_request.text)
    sort_img = pattern.finditer(shop_page_request.text)
    for i in sort_big_img:
        sort_big_img_url = i.group('sort_big_img_url')
        sort_big_img_name = str(sort_big_img_url).lstrip('https://cdn.cnbj1.fds.api.mi-img.com/mi-mall/').split('?')[0]
        sort_img_url_list.append(sort_big_img_url)
        sort_img_name_list.append('小米商城/分类图片/大图/' + sort_big_img_name)
    for i in sort_img:
        sort_img_url = i.group('sort_img_url')
        sort_img_name = str(i.group('img_name')).strip().rstrip('\\t').replace("/", "&") + '.png'
        sort_img_url_list.append(sort_img_url)
        sort_img_name_list.append('小米商城/分类图片/' + sort_img_name)

    # 下载
    loop.run_until_complete(downMain(shop_img_name_list, shop_img_url_list))
    loop.run_until_complete(downMain(sort_img_name_list, sort_img_url_list))



if __name__ == '__main__':
    try:
        # 新建目录,未填路径，只有目录名则默认在当前目录下添加
        os.mkdir('小米官网图片')
    except BaseException:
        pass
    # 修改默认目录
    os.chdir('小米官网图片')

    url = 'https://www.mi.com/'
    heard = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60"}

    # 启动多线程
    loop = asyncio.get_event_loop()

    # 获取首页中各页面的链接
    first_page_request = requests.get(url, headers=heard)
    first_page_xpath = etree.HTML(first_page_request.text)
    first_page_xpath_div = first_page_xpath.xpath('//*[@id="header-wrapper"]/div/nav[1]/div')

    # 将各页面的名字和链接地址存入列表
    name_list = []
    url_list = []
    for div in first_page_xpath_div:
        first_page_xpath_div_a_name = div.xpath('./a/text()')
        name_list.append(first_page_xpath_div_a_name[0])
        first_page_xpath_div_a_url = div.xpath('./a/@href')
        url_list.append(first_page_xpath_div_a_url[0])

    # 创建各页面的资源文件夹
    for name in name_list:
        try:
            os.mkdir(f'{name}')
        except BaseException:
            pass

    # 下载官网首页图片
    first_page()

    # 下载小米商城图片
    shop_page()

