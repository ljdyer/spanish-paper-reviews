"""
01_get_data.py

Get 'evaluation' and 'text' fields for all Spanish-language reviews in the
Paper Reviews Data Set and store in a csv file.

Paper Reviews Data Set: https://archive.ics.uci.edu/ml/datasets/Paper+Reviews
"""

import json
import csv

INPUT_FILE_PATH = "data/reviews.json"
OUTPUT_FILE_PATH = "data/reviews_es.csv"
EXPECTED_NUM_REVIEWS = 405


# ====================
def main():

    # Read and deserialise JSON file
    with open(INPUT_FILE_PATH, "r", encoding='utf-8') as input_file:
        data = json.load(input_file)

    # All data is inside top-level key 'paper'
    papers = data['paper']
    # The data consists of many objects representing single papers, each of
    # which contains 1 or more reviews
    num_reviews = sum([len(paper['review']) for paper in papers])
    # # The dataset description on the website tells us that the dataset has
    # # 405 instances. As a sanity check, confirm that the program is correctly
    # # hitting every instance.
    if num_reviews != EXPECTED_NUM_REVIEWS:
        raise RuntimeError(('The number of reviews is different from the '
                            'expected number. Check that the program is '
                            'hitting every review. '
                            f'(Expected: {EXPECTED_NUM_REVIEWS}; '
                            f'Found: {num_reviews}.)'))
    else:
        print(f'Total number of reviews: {num_reviews}')
    # Get 'text' and 'evaluation' fields for each of the Spanish reviews where
    # 'text' is not empty
    text_eval_pairs = [(review['text'], review['evaluation'])
                       for paper in papers for review in paper['review']
                       if review['lan'] == 'es' and review['text']]
    print(f'Number of (non-empty) Spanish reviews: {len(text_eval_pairs)}')

    # # Write to csv
    with open(OUTPUT_FILE_PATH, "w",
              encoding='utf-8', newline='') as output_file:
        csv_out = csv.writer(output_file)
        csv_out.writerow(['Review', 'Evaluation'])
        csv_out.writerows(text_eval_pairs)
    print(f'{len(text_eval_pairs)} reviews and evaluation scores saved to',
          OUTPUT_FILE_PATH)


# ====================
if __name__ == "__main__":

    main()
