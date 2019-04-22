from pymongo import MongoClient
import pymongo
from math import pow, sqrt

def get_movies_collection():
    # client = MongoClient('mongodb://joseph:live199823@cluster0-shard-00-00-w30lz.mongodb.net:27017,cluster0-shard-00-01-w30lz.mongodb.net:27017,cluster0-shard-00-02-w30lz.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true')
    client = MongoClient()
    movies = client.felkub.movies
    return movies

def get_directors_collection():
    #client = MongoClient('mongodb://joseph:live199823@cluster0-shard-00-00-w30lz.mongodb.net:27017,cluster0-shard-00-01-w30lz.mongodb.net:27017,cluster0-shard-00-02-w30lz.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true')
    client = MongoClient()
    directors = client.felkub.directors
    return directors

def get_genres_collection():
    # client = MongoClient('mongodb://joseph:live199823@cluster0-shard-00-00-w30lz.mongodb.net:27017,cluster0-shard-00-01-w30lz.mongodb.net:27017,cluster0-shard-00-02-w30lz.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true')
    client = MongoClient()
    genres = client.felkub.genres
    return genres

def get_starring_collection():
    # client = MongoClient('mongodb://joseph:live199823@cluster0-shard-00-00-w30lz.mongodb.net:27017,cluster0-shard-00-01-w30lz.mongodb.net:27017,cluster0-shard-00-02-w30lz.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true')
    client = MongoClient()
    stars = client.felkub.starring
    return stars

def get_movies_info_in_some_order(attr, info, order):
    movies_list = list()
    for item in info:
        movies_list.append(item['_id'])
    movies_info = get_movies_collection()
    if order == -1:
        info_list = list()
        for movie in movies_info.find({'_id': {'$in': movies_list}}).sort(attr, pymongo.DESCENDING):
            info_list.append(movie)
        return info_list
    elif order == 1:
        info_list = list()
        for movie in movies_info.find({'_id': {'$in': movies_list}}).sort(attr, pymongo.ASCENDING):
            info_list.append(movie)
        return info_list


def get_directors_info_in_some_order(attr, info, order):
    directors_list = list()
    for item in info:
        directors_list.append(item['_id'])
    directors_info = get_directors_collection()
    if order == -1:
        info_list = list()
        for director in directors_info.find({'_id': {'$in': directors_list}}).sort(attr, pymongo.DESCENDING):
            info_list.append(director)
        return info_list
    elif order == 1:
        info_list = list()
        for director in directors_info.find({'_id': {'$in': directors_list}}).sort(attr, pymongo.ASCENDING):
            info_list.append(director)
        return info_list


def get_starring_info_in_some_order(attr, info, order):
    starring_list = list()
    for item in info:
        starring_list.append(item['_id'])
    starring_info = get_starring_collection()
    if order == -1:
        info_list = list()
        for star in starring_info.find({'_id': {'$in': starring_list}}).sort(attr, pymongo.DESCENDING):
            info_list.append(star)
        return info_list
    elif order == 1:
        info_list = list()
        for star in starring_info.find({'_id': {'$in': starring_list}}).sort(attr, pymongo.ASCENDING):
            info_list.append(star)
        return info_list


def get_sorted_categories():
    movies_info = get_movies_collection()
    category_dict = dict()
    for item in movies_info.find():
        genres = item['Genres']
        for genre in genres:
            if genre in category_dict:
                category_dict[genre] = category_dict[genre] + 1
            else:
                category_dict.setdefault(genre, 1)
    sorted_category_dict = sorted(category_dict.items(), key=lambda d: d[1], reverse=True)
    return sorted_category_dict

def get_movies_of_genre(genre):
    movies_info = get_movies_collection()
    info_list = list()
    for movie in movies_info.find({'Genres': {'$elemMatch': {'$eq': genre}}}):
        info_list.append(movie)
    return info_list

def get_movies_of_nation(nation):
    movies_info = get_movies_collection()
    info_list = list()
    for movie in movies_info.find({'Nation': {'$elemMatch': {'$eq': nation}}}):
        info_list.append(movie)
    return info_list

def get_movies_directed_by(director):
    movies_info = get_movies_collection()
    info_list = list()
    for movie in movies_info.find({'Directors': director}):
        info_list.append(movie)
    return info_list

def get_movies_starred_by(star):
    movies_info = get_movies_collection()
    info_list = list()
    for movie in movies_info.find({'Starring': star}):
        info_list.append(movie)
    return info_list

def search_movie_title(searched):
    movies_info = get_movies_collection()
    info_list = list()
    pattern = '[\s\S]*?' + searched + '[\s\S]*?'
    for movie in movies_info.find({'Title': {'$regex': pattern}}):
        info_list.append(movie)
    return info_list


def advanced_search_movies(title, year_from, year_to, rating_from, rating_to, length_from, length_to):
    movies_info = get_movies_collection()
    info_list = list()
    pattern = '[\s\S]*?' + title + '[\s\S]*?'
    for movie in movies_info.find({
        '$and': [
            {'Title': {'$regex': pattern}},
            {'Year': {'$gte': year_from}},
            {'Year': {'$lte': year_to}},
            {'Rating': {'$gte': rating_from}},
            {'Rating': {'$lte': rating_to}},
            {'Length': {'$gte': length_from}},
            {'Length': {'$lte': length_to}},
        ]
    }):
        info_list.append(movie)
    return info_list


def get_movies_info():
    movies_info = get_movies_collection()
    info_list = list()
    for movie in movies_info.find():
        info_list.append(movie)
    return info_list

def get_directors_info():
    directors_info = get_directors_collection()
    info_list = list()
    for director in directors_info.find():
        info_list.append(director)
    return info_list

def get_starring_info():
    starring_info = get_starring_collection()
    info_list = list()
    for star in starring_info.find():
        info_list.append(star)
    return info_list

def search_directors_name(searched):
    directors_info = get_directors_collection()
    info_list = list()
    pattern = '[\s\S]*?' + searched + '[\s\S]*?'
    for director in directors_info.find({'FullName': {'$regex': pattern}}):
        info_list.append(director)
    return info_list

def search_star_name(searched):
    starring_info = get_starring_collection()
    info_list = list()
    pattern = '[\s\S]*?' + searched + '[\s\S]*?'
    for star in starring_info.find({'FullName': {'$regex': pattern}}):
        info_list.append(star)
    return info_list

def get_sorted_genres_info():
    genres_info = get_genres_collection()
    info_list = list()
    for genre in genres_info.find().sort('Times', pymongo.DESCENDING):
        info_list.append(genre)
    return info_list

def change_genres_traits(name, traits):
    genres_info = get_genres_collection()
    genres_info.update_one(
        {'Name': name},
        {'$set': {'Traits': traits}}
    )

def get_traits_of_genre(name):
    genres_info = get_genres_collection()
    for genre in genres_info.find({'Name': name}):
        return genre['Traits']

def change_movie_traits(imdb, traits):
    movies_info = get_movies_collection()
    movies_info.update_one(
        {'IMDB': imdb},
        {'$set': {'Traits': traits}}
    )

def get_traits_of_movie(imdb):
    movies_info = get_movies_collection()
    movie = movies_info.find_one({'IMDB': imdb})
    return movie['Traits']

def get_similar_movies(id):
    movies_info = get_movies_collection()
    current_movie = movies_info.find_one({'IMDB': id})
    movies_list = list()
    for movie in movies_info.find():
        if movie['IMDB'] == current_movie['IMDB']:
            continue
        common_tags = list()
        common_genres = list()
        common_directors = list()
        common_starring = list()
        for tag in movie['Tags']:
            if tag in current_movie['Tags']:
                common_tags.append(tag)
        for genre in movie['Genres']:
            if genre in current_movie['Genres']:
                common_genres.append(genre)
        for director in movie['Directors']:
            if director in current_movie['Directors']:
                common_directors.append(director)
        for star in movie['Starring']:
            if star in current_movie['Starring']:
                common_starring.append(star)

        whole_num = len(common_tags) + len(common_genres) * 2 + (len(common_directors) + len(common_starring)) * 2.5

        movie['CommonTags'] = common_tags
        movie['CommonGenres'] = common_genres
        movie['CommonDirectors'] = common_directors
        movie['CommonStarring'] = common_starring

        movie['WholeCorrelation'] = whole_num

        if whole_num > 7.0:
            movies_list.append(movie)

    movies_list.sort(key=lambda x: -x["WholeCorrelation"])
    return movies_list

def get_movies_with_related_casts(id):
    movies_info = get_movies_collection()
    current_movie = movies_info.find_one({'IMDB': id})
    common_directors_movies = list()
    common_starring_movies = list()
    both_common_movies = list()

    for movie in movies_info.find({'IMDB': {'$ne': id}}):
        common_directors = list()
        common_starring = list()
        for director in movie['Directors']:
            if director in current_movie['Directors']:
                common_directors.append(director)
        for star in movie['Starring']:
            if star in current_movie['Starring']:
                common_starring.append(star)
        common_starring_num = len(common_starring)
        common_directors_num = len(common_directors)
        common_cast_num = common_starring_num + common_directors_num

        movie['CommonStarring'] = common_starring
        movie['CommonStarringNum'] = common_starring_num
        movie['CommonDirectors'] = common_directors
        movie['CommonDirectorsNum'] = common_directors_num
        movie['CommonCastNum'] = common_cast_num

        if common_directors_num > 0:
            common_directors_movies.append(movie)
        if common_starring_num > 0:
            common_starring_movies.append(movie)
        if common_starring_num > 0 and common_directors_num > 0:
            both_common_movies.append(movie)

    common_directors_movies.sort(key=lambda x: -x["CommonDirectorsNum"])
    common_starring_movies.sort(key=lambda x: -x["CommonStarringNum"])
    both_common_movies.sort(key=lambda x: -(x['CommonCastNum']))

    return common_directors_movies, common_starring_movies, both_common_movies

def get_movies_with_related_tags_and_genres(id):
    movies_info = get_movies_collection()
    current_movie = movies_info.find_one({'IMDB': id})
    common_genres_movies = list()
    common_tags_movies = list()

    for movie in movies_info.find({'IMDB': {'$ne': id}}):
        common_genres = list()
        common_tags = list()
        for genre in movie['Genres']:
            if genre in current_movie['Genres']:
                common_genres.append(genre)
        for tag in movie['Tags']:
            if tag in current_movie['Tags']:
                common_tags.append(tag)
        common_genres_num = len(common_genres)
        common_tags_num = len(common_tags)

        movie['CommonTags'] = common_tags
        movie['CommonTagsNum'] = common_tags_num
        movie['CommonGenres'] = common_genres
        movie['CommonGenresNum'] = common_genres_num

        if common_genres_num > 0:
            common_genres_movies.append(movie)
        if common_tags_num > 0:
            common_tags_movies.append(movie)

    common_genres_movies.sort(key=lambda x: -x["CommonGenresNum"])
    common_tags_movies.sort(key=lambda x: -x["CommonTagsNum"])

    return common_genres_movies, common_tags_movies

def get_director_info_of_name(name):
    directors_info = get_directors_collection()
    director_info = directors_info.find_one({'ShortName': name})
    return director_info

def get_star_info_of_name(name):
    stars_info = get_starring_collection()
    star_info = stars_info.find_one({'ShortName': name})
    return star_info

def get_movies_with_similar_traits(imdb):
    movies_info = get_movies_collection()
    the_movie = movies_info.find_one({'IMDB': imdb})
    the_trait = the_movie['Traits']
    movies = list()
    for movie in movies_info.find({'IMDB': {'$ne': imdb}}):
        traits = movie['Traits']
        distance = 0
        for item in traits.keys():
            value = traits[item]
            the_value = the_trait[item]
            distance = distance + pow(value - the_value, 2)
        distance_root = sqrt(distance)
        movie['Distance'] = round(distance_root, 3)
        movies.append(movie)
    movies.sort(key=lambda x: x['Distance'])
    return movies



def get_traits_translation():
    return {
        'Novelty': '新颖度',
        'AvantGarde': '先锋性',
        'Seriousness': '严肃度',
        'Intimacy': '亲和度',
        'Tensity': '紧张度',
        'Mainstream': '主流度',
        'Obscurity': '抽象性',
        'Artistry': '艺术性'
    }

def get_traits_order():
    return ['Novelty', 'AvantGarde', 'Seriousness', 'Intimacy',
            'Tensity', 'Mainstream', 'Obscurity', 'Artistry']
