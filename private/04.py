"""
get_most_informative_features.py

Get information about the the most informative positive and negative
features (words) for the trained linear regression model.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

MODEL_PATH = "model/bag_of_words_lr.pickle"
FEATURE_LIST_PATH = "model/features.csv"

x = "Me parece un trabajo interesante, con énfasis en cubrir brechas prácticas. Su contenido y estructura están técnicamente bien presentados. Sin embargo, por otro lado, no existe una distinción clara entre los trabajos previos y la propuesta original de este trabajo. El artículo expone que existen trabajos previos respecto a este maridaje CMMI-ÄGIL pero no indica si estas propuestas son suficientes o insuficientes para la mejora. Es decir, la motivación o justificación de este trabajo no está explícita."


# ====================
def save_barplot(data: pd.DataFrame, color: str, title: str, save_path: str,
                 x_box_start: float = 0, negative_coefs: bool = False):
    """Save a barplot of the given data to the path specified."""

    _, ax = plt.subplots(1, 1, figsize=(12, 7))
    sns.barplot(x="Coefficient", y="Feature", data=data,
                palette=reversed(sns.color_palette(f'{color.title()}s_d', 10)))
    ax.set_xlabel("Coefficient", fontsize=14)
    ax.set_ylabel("Feature", fontsize=14)
    # Reverse x axis if plotting negative coefficients
    if negative_coefs:
        ax.invert_xaxis()
    plt.suptitle(title, fontsize=22)
    # Use plt.tight_layout to adjust the position of the plot inside the figure
    # to ensure that axis labels and tick labels fit
    plt.tight_layout(rect=[x_box_start, 0, 1, 1])
    plt.yticks(fontsize=18)
    plt.xticks(fontsize=14)
    plt.savefig(save_path)
    print(f'Plot of "{title}" saved to {save_path}')


# ====================
def main():

    # Unpickle model
    bag_of_words_lr = pickle.load(open(MODEL_PATH, 'rb'))

    # Load csv
    reviews = pd.read_csv('data/reviews_es.csv')

    for row in reviews.iterrows():
        print(bag_of_words_lr.predict([row[1]['Review']]))

    features = pd.read_csv('model/features.csv')

    print(list(reversed(list(features.tail(10)['Feature']))))

    print(bag_of_words_lr.predict([x]))


# ====================
if __name__ == "__main__":

    main()
