#### For CS521 at the University of Illinois, Chicago

# Opinions
## _For Everyone!_

Opinions shows you the happiness/satisfaction index on scale of 1 - 10 for top 500 US universities based on their professors' rating. 
In addition to the universities, you can also find the individual professor rating for any of those universities.

Python with MongoDB for database and React for frontend

## Features
- Select a university from the dropdown
- See its happiness/satisfaction index
- Select a professor from that university
- See his/her rating
- Make your decision

## Tech

Opinions uses many open source technologies to show you what you asked for:

- [ReactJS] - HTML enhanced for web apps!
- [Python] - makes the magic happen
- [mongoDB] - NoSQL db to make our lives easier

And of course Opinions itself is open source for future research.


## Installation

```sh
git clone https://github.com/nehsus/opinions
cd opinions
./run.sh or bash run.sh
```
run.sh:
```sh
#!/bin/bash
echo "Initializing backend.."
cd backend && 
    python3 -m venv opinion_env &&
    source opinion_env/bin/activate &&
    pip3 install -r requirements.txt &&
    echo "done!" &&
    
echo "init ui.." &&
cd ../ &&
    npm install --save &&
    echo "done!" &&
    npm run start
```

## Summary of steps involved:

1. Datatset creation : We created a list of top 500 US universities from sites like US News. Then from RateMyProfessor.com, we scraped data for all the Computer Science department Professors. Data for professors included : names, their average ratings, class ratings,  and all the comments by different students. All this data was stored in MongoDB.

2. UI for University and Professor selection : We created a User Interface to select the university and name of Professor for whom you want to see the opinion score.

![University_selection_page_ui](https://user-images.githubusercontent.com/78128658/163923127-514b6610-471c-4306-9d11-8e9e0067cf9d.jpeg) 

![profesor_selection_screen_ui](https://user-images.githubusercontent.com/78128658/163923315-05affe39-3531-48b6-a2f8-423b63ec6f69.jpeg)

3. Reviews pre-processing : After selecting a Professor name, all the data for the particular Professor is pulled from DB and pre-processed, which involves removal of any bad words and removing all the stop-words from the comments/Reviews.

4. Vader and distilBERT score calculation :  After pre-processing the data, it is fed to the nltk's sentimentIntesityAnalyzer to calculate the normalised score for each comment about the Professor and tag it as positive or negative. Then, average of normalised scores for all the comments is calculated to calculate the rating of the particular Professor. Also, distilBERT model by Flair is also for sentiment analysis of these comments and then an average score is assigned based on that analysis.

5. Comparison of all the scores : Finally after calculating all the scores for the Professors by using different models, we plot a bar-graph to compare our results with that of the existing RateMyProfessor rating, which comes out to be around 80-85% accurate.

6. Rating of University : We also calculate the average rating of the selected university by taking average of the ratings of all the Professors of that University.


## Results
Our Results indicate that the opinions' score is almost 80-85% accurate when compared with the actual RateMyProfessor.com ratings.
The image below shows the comparison of our scores with that of actual RateMyProfessor.com rating for the Professor David Malan:

![Graphical_comparison](https://user-images.githubusercontent.com/78128658/163923272-7d2458bf-b13e-421a-befa-b0665998e284.jpeg)

## Future work
Our work opens up path to many more advancements like comparing Rating of all the Universities based on not only the average Professor ratings but it can also include like class difficulty, Course load etc. We are planning to add more features to this in future and make it more helpful for the students so that they can make a better decision in course selection.:)
