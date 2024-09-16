from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
import numpy as np
import pandas as pd
movies=pd.read_csv(r'C:\Users\manis\Downloads\tmdb_5000_movies.csv')
credits=pd.read_csv(r'C:\Users\manis\Downloads\tmdb_5000_credits.csv')
movies=movies.merge(credits,on='title')
movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]
movies.dropna(inplace=True)
movies.duplicated().sum()
movies.iloc[0].genres
import ast
def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L
movies.genres=movies.genres.apply(convert)
movies.keywords=movies.keywords.apply(convert)

def convert3(obj):
    
    L=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter!=3:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L
movies['cast']=movies['cast'].apply(convert3)

def fetch_director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            L.append(i['name'])
            break
    return L
movies['crew']=movies['crew'].apply(fetch_director)
movies['genres']=movies['genres'].apply(lambda x:[i.replace(' ','')for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(' ','')for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(' ','')for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(' ','')for i in x])
movies['overview']=movies['overview'].apply(lambda x:x.split())
movies['tags']=movies['overview']+movies['genres']+movies['cast']+movies['crew']+movies['keywords']

new_df=movies[['movie_id','title','tags']]
new_df['tags']=new_df['tags'].apply(lambda x:" ".join(x))
new_df['tags']=new_df['tags'].apply(lambda x:x.lower())

cv=CountVectorizer(max_features=5000,stop_words='english')
vector=cv.fit_transform(new_df['tags']).toarray()
cv.get_feature_names_out ()
ps=PorterStemmer()
def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)
new_df['tags']=new_df['tags'].apply(stem)
similarity=cosine_similarity(vector)

def recommend(movie):
    movie_index=new_df[new_df['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    for i in movies_list:
        print(new_df.iloc[i[0]].title)

import pickle
pickle.dump(new_df.to_dict(),open('movie_list.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))
