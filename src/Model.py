import surprise
from surprise import Reader, Dataset
from surprise import dump

class recommender(object):
    
    def __init__(self):
        self.rating_data = None
        self.model = None
        
    
    def read_data(self, data):
        reader = Reader(rating_scale=(1,5))
        self.rating_data = Dataset.load_from_df(data, reader).build_full_trainset()
        
    
    def fit(self):
        # fit model on dataset
        self.model = surprise.SVDpp().fit(self.rating_data)     
    
        
    def recommend(self, new_user_data, n_rec=5, save_model=False):
        self.fit()
        predictions = self.model.test(new_user_data)
        if save_model == True:
            dump.dump('recommender_model', algo=self.model)
        
        # getting predicted rating and song nid
        predictions_ = [(pred.est, pred.iid) for pred in predictions]
        return predictions_

        
    