"""
get_important_features.py

Get information about the the most important positive and negative
features (words) for the trained linear regression model.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

MODEL_PATH = "model/bag_of_words_lr.pickle"
FEATURE_LIST_PATH = "model/features.csv"


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

    # Get lists of features and coefficients and store as a pandas
    # dataframe
    feature_names = (bag_of_words_lr.named_steps['countvectorizer']
                     .get_feature_names_out())
    coefficients = bag_of_words_lr.named_steps['linearregression'].coef_
    most_important = pd.DataFrame(zip(feature_names, coefficients),
                                  columns=['Feature', 'Coefficient'])
    most_important = most_important.sort_values('Coefficient',
                                                ascending=False)

    top_10_positive = most_important.head(10)
    top_10_negative = most_important.tail(10)[::-1]

    # Save barplots of positive and negative features
    save_barplot(data=top_10_positive, color='green',
                 title="Top 10 positive features",
                 save_path='graphs/top_10_positive.png',
                 x_box_start=0.06)
    save_barplot(data=top_10_negative, color='red',
                 title="Top 10 negative features",
                 save_path='graphs/top_10_negative.png',
                 x_box_start=0.05, negative_coefs=True)

    # Save list of features and coefficients to csv
    most_important.to_csv(FEATURE_LIST_PATH, index=False)
    print(f'Features and coefficients saved to {FEATURE_LIST_PATH}')


# ====================
if __name__ == "__main__":

    main()
