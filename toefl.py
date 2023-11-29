import re
import requests
from bs4 import BeautifulSoup
import datetime
import time
from fake_useragent import UserAgent


# 改成自己的
studentID = '114514'
city = 'BEIJING'


# 请求html文件
def askurl(url):
    """"""
    head = {
        "User-Agent":
            "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / "
            "89.0.4389.90Safari / 537.36Edg / 89.0.774.63 ",
        'Cookie': '''改成自己的查询考位的那个请求的Cookie，大概一分钟过期，动作要快'''}
    response = requests.get(url, headers=head)
    print(response.status_code, url)
    html = response.text
    return html

def get_random_user_agent():
    """get random user agent."""
    user_agent = UserAgent()
    return user_agent.random



def getdata(baseurl):
    """"""
    pattern = re.compile(r'<centercode>(.*?)</centercode>')
    html = askurl(baseurl)
    soup = BeautifulSoup(html, "html.parser")
    status = soup.find_all('seatstatus')
    center = soup.find_all('centercode')
    centeravaliable = []
    for j in range(len(status)):
        if str(status[j]) == '<seatstatus>1</seatstatus>':
            centeravaliable.append(re.findall(pattern, str(center[j]))[0])

    return centeravaliable


date = datetime.date(year=2023, month=9, day=1)  # 开始日期
n = 40  # 往后查询多少天
for i in range(n):
    if (date + datetime.timedelta(days=i)).isoweekday() == 2 or (
            date + datetime.timedelta(days=i)).isoweekday() == 3 or (
            date + datetime.timedelta(days=i)).isoweekday() == 7 or (
            date + datetime.timedelta(days=i)).isoweekday() == 7:
        result = getdata(f'https://toefl.neea.cn/myHome/{studentID}/testSeat/queryTestSeats?city={city}&testDay='
                         + (date + datetime.timedelta(days=i)).strftime('%Y-%m-%d'))
        print(result, (date + datetime.timedelta(days=i)).strftime('%Y-%m-%d'))
        time.sleep(0.2)  # 查询间隔时间
