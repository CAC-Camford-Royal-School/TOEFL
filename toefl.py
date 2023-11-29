import re
import requests
from bs4 import BeautifulSoup
import datetime
import time
from fake_useragent import UserAgent


# 改成自己的
studentID = '21430881'
city = 'BEIJING'

# 请求html文件
def askurl(url):
    """"""
    head = {
        "User-Agent": get_random_user_agent(),
        'Cookie': "_gcl_au=1.1.909040028.1694768300; ******=!ax+f3MVc1c0uxPdF6X4dP1ycOKDRhJMHhR6pZstCnPIE77af3JkqTEyz1OGYX62e8SrypNw6pTPR59A=; _gid=GA1.3.594426017.1701246962; JSESSIONID=8463C9AED17C0C7C9D081B8F725BA7E4; ZXFFemgWA2YMO=5fhxu8r4v8rLRmfCzX1k1aq2fpo9E6WqiDQ1W35rCbRCKZ6F_WxPCtP30CD.FbXWkIRd.yrJMWgu92fJ.pmmjvOaELCY3RL2NfDxAuo5WcV9Gm4melsGFyHsQy0.RX8Ms; _ga=GA1.3.1224229334.1694768301; _ga_LV4JL7BVSY=GS1.1.1701246961.13.1.1701247139.0.0.0; ZXFFemgWA2YMP=WSdM_zPnSCtgcUFbz.I4juWEdOrRt.1TV.FO4STD4z3cpPPPYKCoBLjTvNkA3MHRWxQwyDLQkrqKO.4cOh_K61MBxY1DMbmls87SW0eFJ9rXh5TlYIo0jOQMfVyr3d3VQwjeVGOqNIkMrGBD2PVUq03YaSv192jDOL52urNAHQySWKW_.jhnNSyJQvbwcxLegk1ydLnmBGFkwkSbEaYdXKAXzXMw.3gTlsxhZ8Jkc6tueR2gInCO6ClKLOTmrxlnwu6RwaqaKoHcWevuSPqyZk9c5lJ01v1NVIqUTJPaTLClw0RkE4qXOjqHmO.k3WYPJkK9J0bGOruOwAp.TjmXQ.jhDrBJXoJUcqeouKpbMFpUGz5o69NNtAQRP6jOZK2T8TGkppv3N_Ta.SDXiThRAyIVG24UMTYfn7TKCiddQF9"
    }
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


if __name__ == '__main__':
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
