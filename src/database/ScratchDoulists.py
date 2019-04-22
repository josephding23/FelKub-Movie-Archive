import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import urllib
from random import choice, uniform
import pymongo
import re
import traceback
from pymongo import MongoClient


top250url = 'https://movie.douban.com/top250?start='
loginUrl = 'https://accounts.douban.com/login?source=movie'
titlesListPath = 'D:/PycharmProjects/WebCrawlers/data/titles'

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

def get_back_up_movie_info_collection():
    client = MongoClient(connect=False)
    db = client.felkub
    movie_info = db.backup
    return movie_info

def get_directors_info_collection():
    client = MongoClient(connect=False)
    db = client.felkub
    directors_info = db.directors
    return directors_info


def get_starring_info_collection():
    client = MongoClient(connect=False)
    db = client.felkub
    starring_info = db.starring
    return starring_info

def get_doulists_collection():
    client = MongoClient(connect=False)
    db = client.felkub
    doulists = db.doulists
    return doulists


def get_error_collection():
    client = MongoClient(connect=False)
    db = client.felkub
    error_log = db.error_log
    return error_log


def get_existed():
    movie_info = get_movie_info_collection()
    existed_url_list = movie_info.distinct('Url')
    return existed_url_list


def get_undownloaded_pics():
    movie_info = get_movie_info_collection()
    url_list = set()
    for item in movie_info.find({'PicDownloaded': {"$exists": False}}):
        url_list.add((item['PictureUrl'], item['IMDB'], item['Title']))
    return url_list


def get_existed_doulist():
    doulists = get_doulists_collection()
    existed_error_url_list = doulists.distinct('Url')
    return existed_error_url_list


def get_existed_error():
    error_collection = get_error_collection()
    existed_error_url_list = error_collection.distinct('Url')
    return existed_error_url_list


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


def compute_total_num(url_list):
    global total_movie_num
    for url in url_list:
        time.sleep(uniform(1, 2))
        text = get_html_text(url)
        soup = BeautifulSoup(text, 'html.parser')
        try:
            title = soup.find(name='div', attrs={'id': 'content'}).h1.string
            total_num = int(soup.find(name='a', attrs={'class': 'active', 'href': url}).span.string[1:-1])
            print('Number of Movies In', title+':', total_num)
            total_movie_num = total_movie_num + total_num
        except:
            print('Error!', url)
            print(traceback.format_exc())


def scratch_doulist(url):
    if url in get_existed_doulist():
        print('Existed')
        return
    text = get_html_text(url)
    soup = BeautifulSoup(text, 'html.parser')
    doulists_info = get_doulists_collection()
    try:
        title = soup.find(name='div', attrs={'id': 'content'}).h1.string
        total_num = int(soup.find(name='div', attrs={'class': 'doulist-filter'}).a.span.string[1:-1])
        num_pages = int(total_num / 25 + 1)
        crawled = False
        print(title)
        print(total_num)
        print(num_pages)
        print(crawled)
        movie_urls = list()
        for i in range(num_pages):
            movie_urls = movie_urls + get_doulist_pages(url + "?start=" + str(i*25))
            time.sleep(uniform(0.1, 0.2))
            print('\rProgress: {:.2%}'.format((i+1) / num_pages), end='')
        print('\n', movie_urls)

        doulists_info.insert_one({
            'Url': url,
            'Title': title,
            'TotalNum': total_num,
            'PageNum': num_pages,
            'crawled': crawled,
            'MoviesUrl': movie_urls
        })
    except:
        print(traceback.format_exc())


def get_doulists_progress():
    doulists = get_doulists_collection()
    crawled_num = 0
    uncrawled_num = 0
    for item in doulists.find():
        if item['crawled'] == True:
            crawled_num = crawled_num + 1
        else:
            uncrawled_num = uncrawled_num + 1
    return crawled_num / (crawled_num + uncrawled_num)


def get_doulist_pages(url):
    text = get_html_text(url)
    soup = BeautifulSoup(text, 'html.parser')
    url_list = list()
    for item in soup.find_all(name='div', attrs={'class': 'title'}):
        url_list.append(item.a['href'])

    return url_list


def crawl_movie_info(url):
    error_log_collection = get_error_collection()
    movie_info_collection = get_movie_info_collection()
    if url in get_existed():
        print('Already Exists')
        return 0

    text = get_html_text(url)
    soup = BeautifulSoup(text, 'html.parser')
    time.sleep(uniform(0.3, 0.5))
    try:
        title = soup.find(name='span', attrs={'property': 'v:itemreviewed'}).string
        year = int(soup.find(name='span', attrs={'class': 'year'}).string[1:-1])
        pic_url = soup.find(name='a', attrs={'class': 'nbgnbg'}).img['src']
        pic_name = pic_url.split('/')[-1]
        rating = float(soup.find(name='strong', attrs={'class': 'll rating_num', 'property': 'v:average'}).string)
        vote_num = int(soup.find(name='span', attrs={'property': 'v:votes'}).string)
        length = int(soup.find(name='span', attrs={'property': 'v:runtime'})['content'])
        tags = '|'.join(i.string for i in soup.find(name='div', attrs={'class': 'tags-body'}).contents[1::2])

        genres = ''
        for genre in soup.find_all(name='span', attrs={'property': 'v:genre'}):
            genres = genres + genre.string + '|'
        genres = genres[0:-1]

        nation = ''
        for item in soup.find_all(name='span', attrs={'class': 'pl'}):
            if item.string == '制片国家/地区:':
                nation = '|'.join(item.next_sibling.string[1:].split(' / '))

        imdb_id = 0
        for item in soup.find_all(name='a', attrs={'rel': 'nofollow', 'target': '_blank'}):
            if item.string[0:2] == 'tt':
                imdb_id = int(item.string[2:])
        if imdb_id == 0:
            print('Invalid IMDB ID!', title)
            error_log_collection.insert_one({
                'Url': url,
                'Log': 'Invalid IMDB ID'
            })
            return 1

        directors_list = list()
        for item in soup.find_all(name='a', attrs={'rel': 'v:directedBy'}):
            directors_list.append(item.string)
        directors = '|'.join(directors_list)

        starts_list = list()
        for item in soup.find_all(name='a', attrs={'rel': 'v:starring'}):
            starts_list.append(item.string)
        stars = '|'.join(starts_list)

        starring_url = list()
        director_url = list()
        for item in soup.find_all(name='a', attrs={'rel': 'v:directedBy'}):
            _url = 'https://movie.douban.com' + item['href']
            director_url.append(_url)
        for item in soup.find_all(name='a', attrs={'rel': 'v:starring'}):
            _url = 'https://movie.douban.com' + item['href']
            starring_url.append(_url)

        summary = str()
        for item in soup.find_all(name='span', attrs={'class': "", 'property': "v:summary"}):
            str_list = item.contents
            for _str in str_list:
                try:
                    matched = re.findall(r'\u3000\u3000([\s\S]*?)\n', _str)
                    summary += matched[0]
                except TypeError:
                    pass
                except IndexError:
                    pass

        print(title)
        print(year)
        print(pic_url)
        print(pic_name)
        print(rating)
        print(vote_num)
        print(length)
        print(tags)
        print(genres)
        print(nation)
        print(imdb_id)
        print(directors)
        print(director_url)
        print(stars)
        print(starring_url)
        print(summary)
        print(url)

        movie_info_collection.insert_one({
            'Title': title,
            'IMDB': imdb_id,
            'Year': year,
            'Rating': rating,
            'VotingNum': vote_num,
            'Length': length,
            'Nation': nation.split('|'),
            'Genres': genres.split('|'),
            'Tags': tags.split('|'),
            'PictureUrl': pic_url,
            'PicName': pic_name,
            'Directors': directors.split('|'),
            'Starring': stars.split('|'),
            'Summary': summary,
            'Url': url,
            'DirectorsUrls': director_url,
            'StarringUrls': starring_url,
            'Transported': False,
            'celeb_processed': False,
            'PicDownloaded': False
        })

        return 2
    except:
        print('Error!', url)
        print(traceback.format_exc())
        error_log_collection.insert_one({
            'Url': url,
            'Log': traceback.format_exc()
        })
        return 3

def proceed():
    doulists = get_doulists_collection()
    error_num = 0
    existed_num = 0
    inserted_num = 0
    new_error_num = 0
    for doulist in doulists.find({'crawled': False}):
        print(doulist['Title'])
        current_num = 0
        try:
            movie_urls = doulist['MoviesUrl']
            title = doulist['Title']
            doulist_url = doulist['Url']
            total_num = doulist['TotalNum']
            for url in movie_urls:
                flag = crawl_movie_info(url)
                if flag == 0:
                    existed_num = existed_num + 1
                if flag == 1:
                    error_num = error_num + 1
                if flag == 2:
                    inserted_num = inserted_num + 1
                if flag == 3:
                    new_error_num = new_error_num + 1
                    error_num = error_num + 1
                current_num = current_num + 1
                print('\nNo. {} of {}, Progress: {:.2%}'.format(current_num, total_num, current_num / total_num))
                print('Inserted:', inserted_num, 'Existed:', existed_num, 'Error: {} (new: {})'.format(error_num, new_error_num), end='\n\n')
            print(title, 'finished!')
            doulists.update_one(
                {'Url': doulist_url},
                {'$set': {'crawled': True}}
            )
        except:
            print(doulist)
            print(traceback.format_exc())


def crawl_doulists_from_PN():
    doulists_set = set()
    num = 0
    for i in range(24):
        time.sleep(uniform(0.1, 0.2))
        url = 'http://www.pniao.com/DouList/main/Pn' + str(i+1) + '.html'
        text = get_html_text(url)
        soup = BeautifulSoup(text, 'html.parser')
        for item in soup.find_all(name='a', attrs={'rel':'nofollow', 'target':'blank'}):
            print(item['href'])
            doulists_set.add(item['href'])
    doulists = list(doulists_set)
    for doulist in doulists:
        num = num + 1
        scratch_doulist(doulist)
        print('\n Total Progress: {:.2%}'.format((num) / len(doulists)))

def crawl_all_YingZhi_doulists():
    for i in range(11):
        time.sleep(uniform(0.1, 0.2))
        url = 'https://www.douban.com/people/tjz230/doulists/all?start=' + str(i * 20) + '&tag='
        text = get_html_text(url)
        print(text)
        soup = BeautifulSoup(text, 'html.parser')
        try:
            for item in soup.find(name='ul', attrs={'class': 'doulist-list'}).contents:
                _str = str(item)
                # print(_str)
                matched = re.findall(r'<a href="([\s\S]*?)">([\s\S]*?)</a>', _str)
                if len(matched) > 0:
                    scratch_doulist(matched[0][0])
        except:
            print(traceback.format_exc())


def get_sorted_categories():
    movies_info = get_movie_info_collection()
    category_dict = dict()
    category_list = list()
    for item in movies_info.find():
        genres = item['Genres']
        for genre in genres:
            if genre in category_dict:
                category_dict[genre] = category_dict[genre] + 1
            else:
                category_dict.setdefault(genre, 1)
    sorted_category_dict = sorted(category_dict.items(), key=lambda d: d[1], reverse=True)
    print(len(category_dict))
    print(category_list)

def get_sorted_directors():
    movies_info = get_movie_info_collection()
    directors_dict = dict()
    directors_list = list()
    for item in movies_info.find():
        directors = item['Directors']
        for director in directors:
            if director in directors_dict:
                directors_dict[director] = directors_dict[director] + 1
            else:
                directors_dict.setdefault(director, 1)
    sorted_director_dict = sorted(directors_dict.items(), key=lambda d: d[1], reverse=True)
    i = 0
    for (key, value) in sorted_director_dict:
        if key != '' and i < 30:
            directors_list.append(key)
            i = i + 1
    for (director, amount) in sorted_director_dict:
        print(director, amount)
    # print(len(directors_list))
    # print(directors_list)

def remove_invalid_cast():
    movies_info = get_movie_info_collection()
    directors_info = get_directors_info_collection()
    starring_info = get_starring_info_collection()
    for movie in movies_info.find({'ValidDirectors': {'$exists': False}}):
        print(movie['Title'])
        director_urls = movie['DirectorsUrls']
        directors = movie['Directors']
        starring_urls = movie['StarringUrls']
        starring = movie['Starring']

        directors_valid = list()
        starring_valid = list()

        for director in directors:
            count = directors_info.count({'ShortName': director})
            if count > 0:
                directors_valid.append(director)
        for star in starring:
            count = starring_info.count({'ShortName': star})
            if count > 0:
                starring_valid.append(star)

        movies_info.update_one(
            {'_id': movie['_id']},
            {'$set':
                 {
                     'ValidDirectors': directors_valid,
                     'ValidStarring': starring_valid
                 }
            }
        )
        print('Progress: {:.2%}'.format(movies_info.count({'ValidDirectors': {'$exists': True}}) / movies_info.count()))

def transport_traits():
    backup = get_back_up_movie_info_collection()
    movies = get_movie_info_collection()

    for item in movies.find({'Traits': {'$exists': False}}):
        backup_item = backup.find_one({'IMDB': item['IMDB']})
        traits = backup_item['Traits']
        title = item['Title']
        movies.update_one(
            {'IMDB': item['IMDB']},
            {'$set': {'Traits': traits}}
        )
        print(title)
        print('Progress: {:.2%}'.format(movies.count({'Traits': {'$exists': True}}) / movies.count()))

def remove_abundant_items():
    movies = get_movie_info_collection()

    movies.update_many(
        {'celeb_processed': {'$exists': True}},
        {'$unset': {'celeb_processed': '', 'tagsAdded': '', 'genresAdded': ''}}
    )

if __name__ == '__main__':
    transport_traits()