from statistics import mean

from better_profanity import profanity

import nltk

import matplotlib.pyplot as plt

from nltk.sentiment import SentimentIntensityAnalyzer
from flair.models import TextClassifier
from flair.data import Sentence

sia = SentimentIntensityAnalyzer()
classifier = TextClassifier.load('en-sentiment')


def get_bar_graph(professor_name, our_score, rmp_score, flair_score):
    data = {'opinions': our_score, 'RMP': rmp_score, 'FLair': flair_score}
    ratings = list(data.keys())
    values = list(data.values())

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(ratings, values, color='maroon',
            width=0.4)

    plt.xlabel("professor_name")
    plt.ylabel("Ratings out of 5")
    plt.title("Comparing different ratings")
    plt.show()


def get_happiness_score_professor_flair(professor):
    processed_comments = preprocess_comments(list(professor.comments))
    old_range = 2
    new_range = 5
    count = 0
    total = 0
    for j in processed_comments:
        sentence = Sentence(j)
        # print(sentence)
        classifier.predict(sentence)
        label = sentence.labels
        items = str(label[0]).split("→")[1].split(" ")
        # print(items)
        if items[1] == 'POSITIVE':
            old_value = float(items[2][1:len(items[2]) - 1])
        else:
            old_value = -1 * float(items[2][1:len(items[2]) - 1])

        new_value = ((old_value - (-1)) * new_range) / old_range
        total += new_value
        count += 1

    if count > 0:
        total = total / count
    else:
        total = 0

    return total


def get_happiness_score_professor(professor):
    sentiment_intensity_analyzer = sia
    count = 0
    total = 0
    old_range = 2
    new_range = 5
    processed_comments = preprocess_comments(list(professor.comments))
    for comment in processed_comments:
        old_value = sentiment_intensity_analyzer.polarity_scores(comment)["compound"]
        new_value = ((old_value - (-1)) * new_range) / old_range
        total = total + new_value
        count = count + 1

    if count > 0:
        total = total / count
    else:
        total = 0

    return total


def get_happiness_score_university(professors_list):
    count = 0
    total = 0
    for professor in professors_list:
        curr_professor_rating = get_happiness_score_professor(professor)
        if curr_professor_rating != 0:
            total += curr_professor_rating
            count += 1

    return total / count


def preprocess_comments(initial_reviews):
    final_reviews = []
    stopwords = nltk.corpus.stopwords.words("english")
    # initial_reviews = Professor.objects(pid=115496).first().comments
    for s in initial_reviews:
        refined_text = profanity.censor(s)
        tokens = [word for word in refined_text.split() if word.lower() not in stopwords]
        temp = ' '.join(tokens)
        final_reviews.append(temp)

    return final_reviews


def is_positive(comment: str):
    scores = [
        sia.polarity_scores(sentence)["compound"]
        for sentence in nltk.sent_tokenize(comment)
    ]
    print(scores)
    return mean(scores) > 0.2


def get_best_comments(comments):
    best = []
    positive = 0
    size = len(comments)
    print(comments)
    comments = preprocess_comments(comments)
    for i in comments:
        if is_positive(i):
            positive += 1
            best.append(i)

    print(F"{positive / size:.2%} correct")
    return best

#
# if __name__ == "__main__":
#     opinion_score = get_happiness_score_professor(778468)
#     flair_score = get_happiness_score_professor_flair(778468)
#     get_bar_graph("abx", opinion_score, flair_score, 2.5)
#     # print(get_happiness_score_university("Adelphi University"))
# #     # _reviews = preprocess_comments()
# #     # training_model(_reviews)
