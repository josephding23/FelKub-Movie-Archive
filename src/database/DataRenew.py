from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from random import choice, uniform
import time
import arrow

import traceback

myHeaders = ["Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
             "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
             "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
             "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
             "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
             "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
             "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
             "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
             "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
             "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
             "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
             "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
             "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
             "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"]

params = {'User-Agent': choice(myHeaders)}


def get_movie_info_collection():
    client = MongoClient(connect=False)
    db = client.felkub
    movie_info = db.movies
    return movie_info

def get_html_text(url):
    global attributeErrorNum, httpErrorNum
    try:
        proxy = {'https:': '127.0.0.1:1080', 'http:': '127.0.0.1:1080'}
        r = requests.get(url, proxies=proxy)
        r.headers = params
        r.encoding = 'utf-8'
        status = r.status_code
        if status == 404:
            print('404', url)
            return ''
        return r.text
    # ['HTTPError', 'AttributeError', 'TypeError', 'InvalidIMDB']
    except:
        print(url)
        print(traceback.format_exc())

def crawl_movie_info(movie):
    movie_info_collection = get_movie_info_collection()

    text = get_html_text(movie['Url'])
    soup = BeautifulSoup(text, 'html.parser')
    time.sleep(uniform(0.3, 0.5))

    utc = arrow.utcnow()

    date = utc.timestamp

    try:

        rating = float(soup.find(name='strong', attrs={'class': 'll rating_num', 'property': 'v:average'}).string)
        vote_num = int(soup.find(name='span', attrs={'property': 'v:votes'}).string)
        tags = '|'.join(i.string for i in soup.find(name='div', attrs={'class': 'tags-body'}).contents[1::2])

        new_data = {
            'Rating': rating,
            'VotingNum': vote_num,
            'Tags': tags.split('|'),
            'LastModifiedDate': date,
            'LastModifiedStatus': True
        }

        print(movie['Title'])
        print(new_data)

        movie_info_collection.update_one(
            {'_id': movie['_id']},
            {'$set': new_data}
        )

    except:
        print(traceback.format_exc())
        movie_info_collection.update_one(
            {'_id': movie['_id']},
            {'$set':
                 {'LastModifiedDate': date,
                  'LastModifiedStatus': False},
             }
        )


def update_data():
    movies_info = get_movie_info_collection()
    for movie in movies_info.find({'LastModifiedDate': {'$exists': False}}):
        crawl_movie_info(movie)
        print('Progress: {:.2%}'.format(movies_info.count({'LastModifiedDate': {'$exists': True}}) / movies_info.count()))


if __name__ == '__main__':
    update_data()