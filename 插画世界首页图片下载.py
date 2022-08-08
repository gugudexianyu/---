import urllib.request
import re
import os
me = os.getcwd()
print('当前目录：', me)
print('文件保存位置：', me + '\动漫图片')
try:
    #新建目录,未填路径，只有目录名则默认在当前目录下添加
    os.mkdir('动漫图片')
except BaseException:
    pass

try:
    # 修改默认目录，可以通过它实现修改下载文件保存位置
    os.chdir('动漫图片')
    fp = open('remember.txt', 'r')
    num = int(fp.readline())
    fp.close()
except FileNotFoundError:
    fp = open('remember.txt', 'w')
    print(1, file=fp)
    num = 1
    fp.close()
except FileNotFoundError:
    pass
#正则表达式 匹配规则
pattern = '/illust/\w*'
#目标网站首页
url = 'https://www.vilipix.com'
#访问目标网址，并将返回的数据存入‘response’中,数据类型为<class 'http.client.HTTPResponse'>
response = urllib.request.urlopen(url)
#解码，将保存的网站数据转化为str类型
content = response.read().decode('utf-8')
#使用正则表达式进行匹配，将‘content’所有符合规则的字符串存入‘list’,数据类型为list
list = re.findall(pattern, content)
#去重
new_list = []
for lst in list:
    if lst not in new_list:
        new_list.append(lst)
print(new_list)
print('----------------------------------------------------------------------------------------')

fp = open('remember.txt', 'r')
num = int(fp.readline())
fp.close()
for twourl in new_list:
    url2 = 'https://www.vilipix.com'
    # 访问目标网址，并将返回的数据存入‘response’中,数据类型为<class 'http.client.HTTPResponse'>
    response2 = urllib.request.urlopen(url2 + twourl)
    # 解码，将保存的网站数据转化为str类型
    print(twourl)
    content2 = response2.read().decode('utf-8')
    # print(content2)

    pattern2 = '(https://img9.vilipix.com/picture/pages/regular[/\w*]*\.jpg|https://img9.vilipix.com/picture/pages/regular[/\w*]*\.png)'
    list2 = re.findall(pattern2, content2)

    for imageurl in list2:
        urllib.request.urlretrieve(imageurl, f'{num}.jpg')
        num += 1

fp = open('remember.txt', 'w')
print(num, file=fp)
fp.close()

print('下载完成！感谢你的使用！')
print(f'你已经通过本软件下载了{num-1}张图片')
os.system('pause')
