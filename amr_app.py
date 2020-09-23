import pandas as pd
import numpy as np
import random
from src.Model import recommender

def load_dataset():
    # load in dataset
    dataset = pd.read_csv('data/trimmed_rating_2.csv')
    rating_data = pd.read_csv('data/rating_data.csv')
    dataset.drop('Unnamed: 0', axis=1, inplace=True)
    rating_data.drop('Unnamed: 0', axis=1, inplace=True)
    return dataset, rating_data


def get_song_name(iid, dataset):
    # get song name from iid
    titles = list(dataset.product_title.unique())
    nids = list(dataset.product_nid.unique())
    if iid in titles:
        return nids[titles.index(iid)]
    else:
        return titles[nids.index(iid)]

def please_rate(dataset):
    # cold start strategy 1
    # get 100 most rated songs for user to choose from
    songs_to_rate = list(dataset.product_title.value_counts().index[:100])
    print('Please pick 5 songs you would like to rate:')
    for song in songs_to_rate:
        print('--', song)
    
    # new user id is static in this iteration of the app
    new_user_ratings = []
    for n in range(5):
        song = input('Enter song name here: ')
        rating = input('Please rate (1 to 5): ')
        new_rating = [4875689, get_song_name(song, dataset), int(rating)]
        new_user_ratings.append(new_rating)
    return new_user_ratings

def new_rating_to_df(new_rating, rating_data):
    new_user_df = pd.DataFrame(new_rating, columns=['customer_id', 'product_nid', 'star_rating'])
    return pd.concat([rating_data, new_user_df])
    
def final_rec(predictions):
    # generating recommendations. format: [(predicted_rating, song_nid) ... (pred_rating, nid)]
    recs = []
    for n in range(5):
        recs.append(random.choice(sorted(predictions, key=lambda x: x[0], reverse=True)[10:100]))
    return recs




if __name__ == '__main__':
    print('Welcome to Adventurous Music Recommender', '\n', 
          'A music recommender that can help you explore new music', '\n',
         'For questions, please contact haowyang9@gmail.com. Feedbacks are greatly appreciated ;-)', '\n')
    try:
        dataset, rating_data = load_dataset()
    except:
        print('Data not found! Please check if file is in correct path: ~/data/rating_data.csv')
    
    # generating necessary data
    new_user_ratings = please_rate(dataset)
    new_df = new_rating_to_df(new_user_ratings, rating_data)
    all_nids = list(new_df.product_nid.unique())
    
    # removing songs user rated
    for l in new_user_ratings:
        all_nids.remove(l[1])
    
    # prepare data to fit into model
    to_predict = [[4875689, nid, 4] for nid in all_nids]
    
    # get predictions from model
    print('\n', 'Generating recommendations for you...')
    recommender = recommender()
    recommender.read_data(new_df)
    predictions = recommender.recommend(new_user_data=to_predict)
    
    # convert nid to song name
    recs = final_rec(predictions=predictions)
    
    # recommend!
    print('Your recommendations are:', '\n')
    for rec in recs:
        print(get_song_name(rec[1], dataset))
    
    # give user the option to refresh recommendations
    refresh = input("Enter 'r' to refresh recommendations, or 'e' to finish: ")
    sanity = 0
    while refresh == 'r':
        sanity += 1
        if sanity >100:
              break
        recs = final_rec(predictions=predictions)
        for rec in recs:
            print(get_song_name(rec[1], dataset))
        refresh = input("Enter 'r' to refresh recommendations, or 'e' to finish: ")
    
    print('Thank you for using Adventurous Music Recommender! Have a good one :-D')
