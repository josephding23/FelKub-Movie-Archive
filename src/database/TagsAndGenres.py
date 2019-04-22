import requests
from pymongo import MongoClient
from random import choice, uniform
import traceback

def get_movie_info_collection():
    client = MongoClient()
    db = client.felkub
    movie_info = db.movies
    return movie_info

def get_tags_collection():
    client = MongoClient()
    db = client.felkub
    movie_info = db.tags
    return movie_info

def get_genres_collection():
    client = MongoClient()
    db = client.felkub
    movie_info = db.genres
    return movie_info

def initiate_genres():
    movies_info = get_movie_info_collection()
    for item in movies_info.find({'genresAdded': {'$exists': False}}):
        if get_genres_collection().count() == 41:
            return
        print(item['Title'])
        genres = item['Genres']
        for genre in genres:
            genres_info = get_genres_collection()
            if genres_info.count({'Name': genre}) == 0:
                times = movies_info.count({'Genres': genre})
                movies_titles = list()
                movies_ids = list()
                movies_urls = list()
                for item in movies_info.find({'Genres': genre}):
                    movies_titles.append(item['Title'])
                    movies_ids.append(item['_id'])
                    movies_urls.append(item['Url'])
                # print('\nName:', tag, '\nTimes:', times, '\nMovieTitles:', movies_titles)

                genres_info.insert_one({
                    'Name': genre,
                    'Times': times,
                    'MovieTitles': movies_titles,
                    'MovieIds': movies_ids,
                    'MovieUrls': movies_urls
                })

        movies_info.update_one(
            {'_id': item['_id']},
            {'$set': {'genresAdded': True}}
        )

        added = movies_info.count({'genresAdded': True})
        all = movies_info.count()
        print('Progress: {:.2%}\n'.format(added / all))

def initiate_tags():
    movies_info = get_movie_info_collection()
    for item in movies_info.find({'tagsAdded': {'$exists': False}}):
        print(item['Title'])
        tags = item['Tags']
        for tag in tags:
            tags_info = get_tags_collection()
            if tags_info.count({'Name': tag}) == 0:
                times = movies_info.count({'Tags': tag})
                movies_titles = list()
                movies_ids = list()
                movies_urls = list()
                for item in movies_info.find({'Tags': tag}):
                    movies_titles.append(item['Title'])
                    movies_ids.append(item['_id'])
                    movies_urls.append(item['Url'])
                # print('\nName:', tag, '\nTimes:', times, '\nMovieTitles:', movies_titles)

                tags_info.insert_one({
                    'Name': tag,
                    'Times': times,
                    'MovieTitles': movies_titles,
                    'MovieIds': movies_ids,
                    'MovieUrls': movies_urls
                })

        movies_info.update_one(
            {'_id': item['_id']},
            {'$set': {'tagsAdded': True}}
        )

        added = movies_info.count({'tagsAdded': True})
        all = movies_info.count()
        print('Progress: {:.2%}\n'.format(added / all))

def set_original_genres_values():
    traits = {
        'Mainstream': 50.0,
        'Novelty': 50.0,
        'Tensity': 50.0,
        'Obscurity': 50.0,
        'Artistry': 50.0,
        'Intimacy': 50.0,
        'AvantGarde': 50.0,
        'Seriousness': 50.0
    }
    get_genres_collection().update_many(
        {},
        {'$set': {'Traits': traits}}
    )

def set_original_tags_values():

    traits = {
        'Mainstream': 50.0,
        'Novelty': 50.0,
        'Tensity': 50.0,
        'Obscurity': 50.0,
        'Artistry': 50.0,
        'Intimacy': 50.0,
        'AvantGarde': 50.0,
        'Seriousness': 50.0
    }

    get_tags_collection().update_many(
        {},
        {'$set': {'Traits': traits}}
    )

def set_original_movies_values():

    traits = {
        'Mainstream': 50.0,
        'Novelty': 50.0,
        'Tensity': 50.0,
        'Obscurity': 50.0,
        'Artistry': 50.0,
        'Intimacy': 50.0,
        'AvantGarde': 50.0,
        'Seriousness': 50.0
    }

    get_movie_info_collection().update_many(
        {},
        {'$set': {'Traits': traits}}
    )


def get_tags_nums():
    tags_info = get_tags_collection()
    total = tags_info.count()
    more_than_one = tags_info.count({'Times': {'$lte': 1}})
    print(total, more_than_one)

#deserted
def manipulate_traits():
    movies_info = get_movie_info_collection()

    for item in movies_info.find({'Manipulated': {'$exists': False}}):
        print(item['Title'])
        genres = item['Genres']
        tags = item['Tags']
        for tag in tags:
            try:
                tag_traits = get_tags_traits(tag)
                for genre in genres:
                    try:
                        genre_traits = get_genres_traits(genre)
                        for name in genre_traits:
                            tag_traits[name] = tag_traits[name] - 0.1 * (tag_traits[name] - genre_traits[name])
                    except:
                        print(traceback.format_exc())
                set_tags_traits(tag, tag_traits)
            except:
                print(traceback.format_exc())
        movies_info.update_one(
            {'_id': item['_id']},
            {'$set': {'Manipulated': 1}}
        )

        print('Progress: {:.2%}\n'.format(movies_info.count({'Manipulated': {'$exists': True}}) / movies_info.count()))


def get_genres_traits(genre):
    genre_info = get_genres_collection().find_one({'Name': genre})
    return genre_info['Traits']

def get_movie_traits(imdb):
    movies_info = get_movie_info_collection().find_one({'IMDB': imdb})
    return movies_info['Traits']

def set_tags_traits(tag, traits):
    get_tags_collection().update_one(
        {'Name': tag},
        {'$set': {'Traits': traits}}
    )


def get_tags_traits(tag):
    tag_info = get_tags_collection().find_one({'Name': tag})
    return tag_info['Traits']

def process():
    initiate_genres()


if __name__ == '__main__':
    set_original_movies_values()
    set_original_tags_values()
    set_original_genres_values()
