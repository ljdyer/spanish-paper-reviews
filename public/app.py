"""
app.py

Main program for Spanish Paper Reviews Flask app.

Show predicted evaluation scores for Spanish-language paper reviews entered
into the text area by the user."""

import pickle

import pandas as pd
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

MODEL_PATH = "model/bag_of_words_lr.pickle"
bag_of_words_lr = pickle.load(open(MODEL_PATH, 'rb'))


# ====================
def get_recommended_score(raw_score: float) -> str:
    """Return the closest valid evaluation score to the raw model
    prediction to get the recommended evluation score

    Valid evaluation scores are integers between -2 and 2"""

    valid_scores = list(range(-2, 3))
    distances = [abs(raw_score - v) for v in valid_scores]
    return valid_scores[distances.index(min(distances))]


# ====================
@app.route('/')
def index():
    """Render index.html on app launch"""

    return render_template('index.html')


# ====================
@app.route('/get_features', methods=['POST'])
def get_features():
    """Return lists of model features (words) with names of color classes
    used to configure text area highlighting."""

    classes_and_features = {}
    feature_df = pd.read_csv('model/features.csv')
    # Positive features (green highlight)
    for i in range(1, 5):
        these_features = feature_df.loc[(feature_df['Coefficient'] > (i-1)/10)
                                        & (feature_df['Coefficient'] < i/10)]
        features = these_features['Feature'].tolist()
        class_name = f'green{i}'
        if features:
            classes_and_features[class_name] = features
    for i in range(1, 9):
        these_features = feature_df.loc[(feature_df['Coefficient'] > (-i-1)/10)
                                        & (feature_df['Coefficient'] < -i/10)]
        features = these_features['Feature'].tolist()
        class_name = f'red{i}'
        if features:
            classes_and_features[class_name] = features

    return jsonify(classes_and_features)


# ====================
@app.route('/get_scores', methods=['POST'])
def get_proba():
    """Return raw and recommended model score in response to
    request containing text input by the user"""

    input_text = request.data
    input_text = input_text.decode('utf-8')
    raw_score = bag_of_words_lr.predict([str(input_text)])[0]
    return jsonify({
        'raw_score': f'{raw_score:.2f}',
        'recommended_score': get_recommended_score(raw_score)
    })


# ====================
if __name__ == "__main__":

    app.run(debug=True)
