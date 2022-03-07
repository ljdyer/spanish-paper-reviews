import math
import pickle

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

MODEL_PATH = "model/bag_of_words_lr.pickle"
bag_of_words_lr = pickle.load(open(MODEL_PATH, 'rb'))





# ====================
def round_score(raw_score: float) -> str:

    if raw_score > 2:
        return '2'
    elif raw_score < -2:
        return '-2'
    else:
        return str(round(raw_score))


# ====================
@app.route('/')
def index():
    """Render index.html on app launch"""

    return render_template('index.html')


# # ====================
@app.route('/get_proba', methods=['POST'])
def get_proba():
    """Return dictionary of category probabilities as a JSON object in response
    to requests containing text input by user"""

    input_text = request.data
    raw_score = bag_of_words_lr.predict([str(input_text)])[0]
    print(raw_score)
    return jsonify({
        'raw_score': f'{raw_score:.2f}',
        'rounded_score': round_score(raw_score)
    })


# ====================
if __name__ == "__main__":

    app.run(debug=True)
