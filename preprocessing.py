from better_profanity import profanity

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def training_model(reviews):
    print("hello")
    data = ["I love you", "I hate you"]
    sentimentIntensityAnalyzer = SentimentIntensityAnalyzer()
    for r in reviews:
        words: list[str] = nltk.word_tokenize(r)
        print(sentimentIntensityAnalyzer.polarity_scores(r))

        # fd = nltk.FreqDist(words)
        # lower_fd = nltk.FreqDist([w.lower() for w in fd])
        # lower_fd.tabulate()
        # print(fd.most_common(3))

    #print(model.summary())


def preprocess_comments(initial_reviews):
    final_reviews = []
    stopwords = nltk.corpus.stopwords.words("english")

    for s in initial_reviews:
        refined_text = profanity.censor(s)
        tokens = [word for word in refined_text.split() if word.lower() not in stopwords]
        temp = ' '.join(tokens)
        final_reviews.append(temp)

    print(final_reviews)
    return final_reviews


if __name__ == "__main__":
    reviews = [
        "Relatively fucked-up class, most stupid assignments could be completed by following step by step instructions from the "
        "PDFs",
        "13-14 assignments but are relatively easy. Can refer the textbook for the course and the lectures are also "
        "good. No exams. Grading based on assignments, guided project and one research highlight (a custom project "
        "based on one research paper or summary of 5 research papers). Easy A.",
        "I'm currently in NLP and I have to say I'm genuinely disappointed. I have a deep love for math and for the "
        "beauty of AI. Unfortunately, I've spent most of my time in this class writing plans for a chatbot design("
        "worst project ever) and doing trial and error on assignments. This class can outright be taught better "
        "across the board."]

    final_reviews = preprocess_comments(reviews)
    training_model(final_reviews)
