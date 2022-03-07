"""
build_model.py

Build a linear regression model with binary unigram bag-of-words features to
predict evaluation scores from review text for Spanish-languages reviews from
the Paper Reviews Data Set.

Paper Reviews Data Set: https://archive.ics.uci.edu/ml/datasets/Paper+Reviews
"""

import pickle

import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline

DATA_PATH = 'data/reviews_es.csv'
PICKLE_PATH = "model/bag_of_words_lr.pickle"


# ====================
def main():

    all_data = pd.read_csv(DATA_PATH)

    # Get Spanish stopwords
    spanish_stopwords = stopwords.words('spanish')

    # Define stemmer function to use as custom CountVectorizer tokenizer
    spanish_stemmer = SnowballStemmer('spanish', ignore_stopwords=True)

    def stemmer(doc):
        tokens = word_tokenize(doc, language='spanish')
        return [spanish_stemmer.stem(token)
                for token in tokens if len(token) > 1]

    # Define model pipeline
    bag_of_words_lr = make_pipeline(
        CountVectorizer(binary=True),
        LinearRegression()
    )

    # Prepare training data
    X, y = all_data.Review, all_data.Evaluation

    # Carry out grid search cross-validation
    param_grid = {
        'countvectorizer__stop_words': [spanish_stopwords, None],
        'countvectorizer__min_df': [1, 2, 3],
        'countvectorizer__max_df': [0.8, 0.9, 1.0],
        'countvectorizer__tokenizer': [stemmer, None],
    }
    grid_search_cv = GridSearchCV(bag_of_words_lr, param_grid)
    grid_search_cv.fit(X, y)
    best_params = grid_search_cv.best_params_
    print('Best parameters from grid search cross-validation:',
          best_params)
    print('Best score from grid search cross-validation:',
          grid_search_cv.best_score_)
    print()

    # Fit model using best parameters
    bag_of_words_lr.set_params(**best_params)
    bag_of_words_lr.fit(X, y)

    # Pickle the model
    pickle.dump(bag_of_words_lr, open(PICKLE_PATH, 'wb'))
    print(f'Model pickled as {PICKLE_PATH}')


# ====================
if __name__ == "__main__":

    main()
