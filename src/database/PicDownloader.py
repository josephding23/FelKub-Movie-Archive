import requests
from pymongo import MongoClient
from random import choice, uniform
import time
import os
import PIL.Image as Image

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
    client = MongoClient()
    db = client.felkub
    movie_info = db.movies
    return movie_info

def get_directors_info_collection():
    client = MongoClient()
    db = client.felkub
    movie_info = db.directors
    return movie_info

def get_starring_info_collection():
    client = MongoClient()
    db = client.felkub
    movie_info = db.starring
    return movie_info


def get_unsuccessful_pics():
    picDir = 'F:/douban/'
    movies_info = get_movie_info_collection()
    os.chdir(picDir)
    unsuccess = list()
    picList = os.listdir(picDir)
    for item in movies_info.find():
        picName = item['PicName']
        picFile = picDir + picName
        if not os.path.isfile(picFile):
            unsuccess.append(picName)
        if os.path.isfile(picFile):
            if os.path.getsize(picFile) < 1000:
                unsuccess.append(picName)
    print(len(unsuccess))
    return unsuccess


def pic_downloader():
    from urllib.parse import urlsplit
    movies_info = get_movie_info_collection()
    # celeb_info = get_movie_info_collection()
    total_num = movies_info.count()
    root = 'D:/PycharmProjects/FelKubArchive/pic/movies/large/'
    for item in movies_info.find({'PicDownloaded': False}):
        url = item['PictureUrl']
        # pic_name = urlsplit(url).path.split('/')[-1]
        path = root + item['PicName']
        if os.path.isfile(path):
            if os.path.getsize(path) > 0:
                continue
        else:
            print(item['Title'])

            html = requests.get(url, params=params)

            with open(path, 'wb') as file:
                file.write(html.content)
            time.sleep(uniform(0.2, 1))


            movies_info.update_one(
                {'PictureUrl': url},
                {'$set': {'PicDownloaded': True}}
            )

            downloaded = movies_info.count({'PicDownloaded': True})
            print('Progress: {:.2%}'.format(downloaded / total_num), '\n')


def download_cleaner():
    import urllib.request
    unsuccess = get_unsuccessful_pics()
    total = len(unsuccess)
    movies_info = get_movie_info_collection()
    i = 0
    for pic in unsuccess:
        i = i + 1
        url = movies_info.find({'PicName': pic})[0]['PictureUrl']
        time.sleep(uniform(0.1, 0.3))
        try:
            content = urllib.request.urlopen(url).read()
            path = 'F:/douban/' + pic
            with open(path, 'wb') as file:
                file.write(content)
            print('Downloaded:', pic)
        except:
            print('Error:', pic)
        print('Progress: {} of {}'.format(i, total))


def picResizer():
    directors_info = get_directors_info_collection()
    picDir = 'D:/PycharmProjects/FelKubArchive/pic/movies/large/'
    picList = os.listdir(picDir)
    for item in picList:
        picName = item
        oriPath = 'D:/PycharmProjects/FelKubArchive/pic/movies/large/' + picName
        newPath = 'D:/PycharmProjects/FelKubArchive/pic/movies/small/' + picName
        try:
            sImg = Image.open(oriPath)
            if not os.path.isfile(newPath):
                try:
                    dImg = sImg.resize((108, 160), Image.ANTIALIAS)
                    dImg.save(newPath)
                    print(newPath)
                except:
                    print(newPath)
            elif os.path.isfile(newPath):
                if os.path.getsize(newPath) == 0:
                    try:
                        dImg = sImg.resize((108, 160), Image.ANTIALIAS)
                        dImg.save(newPath)
                        print(newPath)
                    except:
                        print(newPath)
        except:
            pass

if __name__ == '__main__':
    # print(os.path.getsize('F:/douban/p453506001.jpg'))
    picResizer()