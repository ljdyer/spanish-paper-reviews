# Spanish paper review evaluation predictor

A website to demonstrate the results of a University assignment to build a linear regression model with binary unigram bag-of-words features to predict evaluation scores trained using Spanish-language paper reviews from the [Paper Reviews Data Set](https://archive.ics.uci.edu/ml/datasets/Paper+Reviews).

## How to use it

Go to https://spanish-paper-reviews.herokuapp.com/.

Type some Spanish words into the text area, or paste a review from [the dataset](private/data/reviews_es.csv) to see the raw model prediction and recommended evaluation score (the nearest integer between -2 and 2).

Features (words) that appear in the dataset will be highlighted. Positive features are highlighted in green and negative features are highlighted in red. The more important a feature (the higher the absolute value of its coefficient in the trained linear regression model), the darker the highlight.

<a href="https://spanish-paper-reviews.herokuapp.com/"><img src="readme-img.PNG"></img></a>

## How it works

(more documentation to follow)

## Credits

Text area highlights implemented using [highlight-within-textarea](https://github.com/lonekorean/highlight-within-textarea) plugin.