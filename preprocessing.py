from better_profanity import profanity

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

from model import Professor, University


def get_happiness_score_professor(professor_name):
    sentiment_intensity_analyzer = SentimentIntensityAnalyzer()
    professor = Professor.objects(name=professor_name).first()
    # print(professor.comments)
    count = 0
    total = 0
    old_range = 2
    new_range = 5
    processed_comments = preprocess_comments(professor.comments)
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


def get_happiness_score_university(university_name):
    sentiment_intensity_analyzer = SentimentIntensityAnalyzer()
    university = University.objects(title=university_name).first()

    professors_list = list(Professor.objects(university=university))
    count = 0
    total = 0
    for professor in professors_list:
        curr_professor_rating = get_happiness_score_professor(professor.name)
        if curr_professor_rating != 0:
            total += curr_professor_rating
            count += 1

    print(total)
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


if __name__ == "__main__":

    print(get_happiness_score_professor("Salvatore Ferrugia"))
    # print(get_happiness_score_university("Adelphi University"))
    # _reviews = preprocess_comments()
    # training_model(_reviews)
