import requests
from bs4 import BeautifulSoup
from random import choice, uniform
import pymongo
import traceback
import re
import time
from pymongo import MongoClient

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
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20"]

params = {'User-Agent': choice(myHeaders)}
proxy = {'https:': '127.0.0.1:1080', 'http:': '127.0.0.1:1080'}

def get_html_text(url):
    r = requests.get(url, params=params)
    # r.headers = params
    r.encoding = 'utf-8'
    return r.text

def get_movie_info_collection():
    client = MongoClient()
    # client = MongoClient('mongodb://joseph:live199823@cluster0-shard-00-00-w30lz.mongodb.net:27017,cluster0-shard-00-01-w30lz.mongodb.net:27017,cluster0-shard-00-02-w30lz.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true')
    db = client.felkub
    movie_info = db.movies
    return movie_info


def get_directors_info_collection():
    client = MongoClient()
    # client = MongoClient('mongodb://joseph:live199823@cluster0-shard-00-00-w30lz.mongodb.net:27017,cluster0-shard-00-01-w30lz.mongodb.net:27017,cluster0-shard-00-02-w30lz.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true')
    db = client.felkub
    directors_info = db.directors
    return directors_info

def get_starring_info_collection():
    # client = MongoClient('mongodb://joseph:live199823@cluster0-shard-00-00-w30lz.mongodb.net:27017,cluster0-shard-00-01-w30lz.mongodb.net:27017,cluster0-shard-00-02-w30lz.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true')
    client = MongoClient()
    db = client.felkub
    starring_info = db.starring
    return starring_info

'''
def get_celeb_exists_list():
    celebrity_info = get_celeb_info_collection()
    celeb_lists = celebrity_info.distinct('Url')
    return celeb_lists
'''


def get_unprocessed_movie_url():
    movie_info = get_movie_info_collection()
    url_list = set()
    for item in movie_info.find({'DirectorUrls': {"$exists": False}}):
        url_list.add((item['Title'], item['Url']))
    return url_list


def get_total_number():
    movie_info = get_movie_info_collection()
    movie_set = set()
    for item in movie_info.find():
        movie_set.add(item)
    return len(movie_set)


def scratch_movie_celebs(movie):
    url = movie['Url']
    print(url)
    try:
        text = get_html_text(url)
    except:
        print(traceback.format_exc())
        return
    soup = BeautifulSoup(text, 'html.parser')
    movie_info = get_movie_info_collection()
    starring_url = list()
    director_url = list()
    try:
        for item in soup.find_all(name='a', attrs={'rel': 'v:directedBy'}):
            _url = 'https://movie.douban.com' + item['href']
            director_url.append(_url)
        for item in soup.find_all(name='a', attrs={'rel': 'v:starring'}):
            _url = 'https://movie.douban.com' + item['href']
            starring_url.append(_url)
    except:
        print(traceback.format_exc())


    '''
    print('\nDirector(s): \n')
    len_directors = len(director_set)
    for index in range(len_directors):
        director_url = director_set[index]
        print('{} of {}'.format(index+1, len_directors))
        flag = True
        if director_url not in get_celeb_exists_list():
            print(director_url)
            time.sleep(uniform(0.1, 0.4))
            flag = scratch_celebrity_info(director_url)
        time.sleep(uniform(0.4, 0.6))
        if flag:
            add_title_and_role_to_celebrity(director_url, url, title, 'director')

    len_stars = len(starring_set)
    print('\nStarring(s): \n')
    for index in range(len_stars):
        starring_url = starring_set[index]
        print('{} of {}'.format(index+1, len_stars))
        flag = True
        if starring_url not in get_celeb_exists_list():
            print(starring_url)
            time.sleep(uniform(0.2, 0.5))
            flag = scratch_celebrity_info(starring_url)
        time.sleep(uniform(0.3, 0.6))
        if flag:
            add_title_and_role_to_celebrity(starring_url, url, title, 'starring')
    '''

    print(movie['Title'])
    movie_info.update_one(
        {'_id': movie['_id']},
        {'$set': {'DirectorsUrls': director_url, 'StarringUrls': starring_url, 'urls_got': True}})

'''
def add_title_and_role_to_celebrity(url, movie_url, title, role):
    item_role_dict = {'director': 'DirectedMovies', 'starring': 'StarredMovies'}
    item_urls_dict = {'director': 'DirectedUrls', 'starring': 'StarredUrls'}
    celebrity_info = get_celeb_info_collection()
    fields = celebrity_info.find_one({'Url': url})
    print('Celebrity', fields['Name'], 'added')
    print('Title:', title, 'Role:', role, '\n')
    celebrity_info.update_one(
        {'Url': url},
        {'$addToSet': {item_role_dict[role]: title, item_urls_dict[role]: movie_url}}
    )
    print('Updated')
'''

def scratch_celebrity_info(celeb):

    url = celeb['Url']
    if 'subject_search?' in url:
        # celebrity_info = get_directors_info_collection()
        celebrity_info = get_starring_info_collection()
        celebrity_info.update_one(
            {'Url': celeb['Url']},
            {'$set':
                {
                    'Crawled': True,
                    'Unexist': True
                }
            }
        )
        return True
    time.sleep(uniform(0.1, 3.5))
    text = get_html_text(url)
    soup = BeautifulSoup(text, 'html.parser')
    try:
        Name = soup.find(name='h1').string
    except Exception:
        print(celeb['ShortName'])
        celebrity_info = get_starring_info_collection()
        celebrity_info.update_one(
            {'Url': celeb['Url']},
            {'$set':
                {
                    'Crawled': True,
                    'Unexist': True
                }
            }
        )
        return True
    tags_list = list()
    info_list = list()
    Summary = str()
    PicUrl = str()
    tags_dict = {'性别': 'Sex', '出生日期': 'BirthDate', '出生地': 'BirthPlace', '职业': 'Occupation'}
    try:
        for item in soup.find(name='div', attrs={'class': 'info'}).ul.children:
            for field in re.findall(r'<span>([\s\S]*?)</span>', str(item)):
                if len(field) > 0:
                    tags_list.append(field)
            for field in re.findall(r'</span>: \n\s+([\s\S]*?)\n\s+</li>', str(item)):
                if len(field) > 0:
                    info_list.append(field)
    except Exception:
        print(celeb['ShortName'])
        print(traceback.format_exc())

    try:
        for item in soup.find_all(name='span', attrs={'class': "all hidden"}):
            str_list = item.contents
            # print(str_list)
            for _str in str_list:
                # print(_str)
                try:
                    matched = re.findall(r'\u3000\u3000([\s\S]*?)$', _str)
                    # print(matched)
                    Summary += matched[0]
                except TypeError:
                    pass
                except IndexError:
                    pass
        if Summary == '':
            for item in soup.find_all(name='div', attrs={'class': 'bd'}):
                str_list = item.contents
                for _str in str_list:
                    try:
                        matched = re.findall(r'\u3000\u3000([\s\S]*?)\n', _str)
                        Summary += matched[0]
                    except TypeError:
                        pass
                    except IndexError:
                        pass
    except Exception:
        print('Summary Error!')

    try:
        PicUrl = soup.find(name='img', attrs={'title': '点击看大图'})['src']
    except Exception:
        PicUrl = 'https://img3.doubanio.com/f/movie/8dd0c794499fe925ae2ae89ee30cd225750457b4/pics/movie/celebrity-default-medium.png'

    Sex = str()
    BirthDate = str()
    BirthPlace = str()
    Occupations = list()
    for index in range(min(len(tags_list), len(info_list))):
        tag = tags_list[index]

        if tag in tags_dict:
            tag = tags_dict[tags_list[index]]
            info = info_list[index]
            if tag == 'Sex':
                Sex = info
            if tag == 'BirthDate':
                BirthDate = info
            if tag == 'BirthPlace':
                BirthPlace = info
            if tag == 'Occupation':
                Occupations = info_list[index].split(' / ')

    print('\nName:', Name)
    print('Sex:', Sex)
    print('BirthDate:', BirthDate)
    print('BirthPlace:', BirthPlace)
    print('Occupation:', Occupations)
    print('Summary:', Summary)
    print('PicUrl:', PicUrl)

    # celebrity_info = get_directors_info_collection()
    celebrity_info = get_starring_info_collection()

    celebrity_info.update_one(
        {'Url': celeb['Url']},
        {'$set':
            {
                'FullName': Name,
                'Sex': Sex,
                'BirthPlace': BirthPlace,
                'BirthDate': BirthDate,
                'Occupation': Occupations,
                'PicUrl': PicUrl,
                'Summary': Summary,
                'Crawled': True
            }
        }
    )

    return True


def add_celeb_url_to_movie_collection():
    movies = get_movie_info_collection()
    num = 0
    for field in movies.find({'DirectorsUrls': {'$exists': False}}):
        num = num + 1
        time.sleep(uniform(0.1, 0.3))
        scratch_movie_celebs(field)
        processed = movies.count({'DirectorsUrls': {'$exists': True}})
        all = movies.count()
        print('\nProgress: {:.2%}\n'
              .format(processed / all))

def get_existed_directors():
    directors_info = get_directors_info_collection()
    existed = directors_info.distinct('Url')
    return existed

def crawl_directors_info():
    directors_info = get_directors_info_collection()
    for item in directors_info.find({'Crawled': False}):
        scratch_celebrity_info(item)
        print_progress()

def crawl_starring_info():
    starring_info = get_starring_info_collection()
    for item in starring_info.find({'Crawled': False}):
        scratch_celebrity_info(item)
        print_progress()

def print_progress():
    # celebrity_info = get_directors_info_collection()
    celebrity_info = get_starring_info_collection()
    processed = celebrity_info.count({'Crawled': True})
    all = celebrity_info.count()
    print('Progress: {:.2%}'.format(processed / all))


def get_existed_starrings():
    starring_info = get_starring_info_collection()
    existed = starring_info.distinct('Url')
    return existed

def print_celeb_progress():
    movies_info = get_movie_info_collection()
    processed = movies_info.count({'celeb_processed': True})
    all = movies_info.count()
    print('Progress: {:.2%}'.format(processed / all))

def add_celebrity_attributes():
    celebrity_info = get_starring_info_collection()
    movies_info = get_movie_info_collection()
    for celeb in celebrity_info.find({'AverageActiveYear': {'$exists': False}}):
        total_votes = 0
        total_year = 0
        for movie in movies_info.find({'Starring': celeb['ShortName']}):
            vote = movie['VotingNum']
            year = movie['Year']
            total_votes = total_votes + vote
            total_year = total_year + year

        total_num = movies_info.count({'Starring': celeb['ShortName']})

        average_year = round(total_year / total_num, 3)

        print(celeb['ShortName'], total_votes, average_year)

        celebrity_info.update_one(
            {'_id': celeb['_id']},
            {'$set':
                {
                    'AverageActiveYear': average_year,
                    'TotalVotes': total_votes
                }
            }
        )

        processed = celebrity_info.count({'AverageActiveYear': {'$exists': True}})
        all = celebrity_info.count()
        print('Progress: {:.2%}'.format(processed / all))

def initiate_celebs():
    movies_info = get_movie_info_collection()
    directors_collection = get_directors_info_collection()
    starring_collection = get_starring_info_collection()
    for item in movies_info.find({'celeb_processed': False}):
        title = item['Title']
        print(title, '\n')
        directors = item['Directors']
        starring = item['Starring']
        director_urls = item['DirectorsUrls']
        starring_urls = item['StarringUrls']

        direct_size = min(len(director_urls), len(directors))
        star_size = min(len(starring_urls), len(starring))

        for i in range(direct_size):
            if director_urls[i] in get_existed_directors():
                # print('Existed!')
                continue
            else:
                times = 0
                director_name = directors[i]
                director_url = director_urls[i]
                movie_ids = list()
                movie_titles = list()
                movie_urls = list()
                for movie in movies_info.find({'Directors': director_name}):
                    movie_ids.append(movie['_id'])
                    movie_titles.append(movie['Title'])
                    movie_urls.append(movie['Url'])
                    times = times + 1
                '''
                print('Name:', director_name, '\nUrl:', director_url, '\nMovie Names:', movie_titles,
                      '\nMovie ids:', movie_ids, '\nMovie urls:', movie_urls, '\nTimes:', times, '\n')
                '''
                if times > 2:
                    directors_collection.insert_one({
                        'ShortName': director_name,
                        'Url': director_url,
                        'DirectedTitles': movie_titles,
                        'DirectedUrls': movie_urls,
                        'DirectedIds': movie_ids,
                        'DirectNum': times,
                        'Crawled': False
                    })

        for i in range(star_size):
            if starring_urls[i] in get_existed_starrings():
                # print('Existed!')
                continue
            else:
                times = 0
                star_name = starring[i]
                star_url = starring_urls[i]
                movie_ids = list()
                movie_titles = list()
                movie_urls = list()
                for movie in movies_info.find({'Starring': star_name}):
                    movie_ids.append(movie['_id'])
                    movie_titles.append(movie['Title'])
                    movie_urls.append(movie['Url'])
                    times = times + 1
                '''
                print('Name:', star_name, '\nUrl:', star_url, '\nMovie Names:', movie_titles,
                      '\nMovie ids:', movie_ids, '\nMovie urls:', movie_urls, '\nTimes', times, '\n')
                '''
                if times > 2:
                    starring_collection.insert_one({
                        'ShortName': star_name,
                        'Url': star_url,
                        'StarredTitles': movie_titles,
                        'StarredUrls': movie_urls,
                        'StarredIds': movie_ids,
                        'StarNum': times,
                        'Crawled': False
                    })

        movies_info.update_one(
            {'_id': item['_id']},
            {'$set': {'celeb_processed': True}}
        )

        print_celeb_progress()

def delete_the_less():
    directors_info = get_directors_info_collection()
    starring_info = get_starring_info_collection()
    directors_info.delete_many({'DirectNum': {'$lt': 3}})
    # starring_info.delete_many({'StarNum': {'$lt': 3}})

def process():
    # ignite_scratching()
    # crawl_directors_info()
    # crawl_starring_info()
    add_celebrity_attributes()

if __name__ == '__main__':
    # scratch_movie_celebs('https://movie.douban.com/subject/26588308/')
    # scratch_celebrity_info('https://movie.douban.com/celebrity/1054443/')

    process()
    # scratch_movie_celebs('https://movie.douban.com/subject/1291832/', '低俗小说 Pulp Fiction')
    # scratch_movie_celebs('https://movie.douban.com/subject/6307447/', '被解救的姜戈 Django Unchained')
    # unset_fields()
    # print(len(get_updated_celeb_movie_url()))
    # print(get_celeb_exists_list())
    # print_directors_progress()
