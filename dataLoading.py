from os import stat
from pandas.io.stata import stata_epoch
from py2neo import Graph
import pandas as pd
import numpy as np
import math

f =open("data.cypher",'w',encoding="utf-8")

# # Creating Database
f.write("DROP DATABASE recommendersystem IF EXISTS DUMP DATA;\n")
f.write("CREATE DATABASE recommendersystem IF NOT EXISTS;\n")
f.write(":USE recommendersystem;\n")

movies = pd.read_csv("movie_dataset.csv",encoding="utf-8")
# print(movies)

# # Constrains in movie nodes
statement = "CREATE CONSTRAINT movies_key ON (x:Movies) ASSERT (x.movie_id) IS NODE KEY;\n" 
f.write(statement)

statement = "CREATE CONSTRAINT movies_title_notnull ON (p:Movies) ASSERT exists(p.title);\n"
f.write(statement)

# We are creating movies nodes

for rows in range(len(movies)):
    movie_id = rows
    title = movies['movie_title'][rows]
    url = movies['movie_imdb_link'][rows]
    duration = "NULL" if pd.isna(movies['duration'][rows]) else movies['duration'][rows]
    if not pd.isna(movies['title_year'][rows]):
        try:
            year = int(movies['title_year'][rows])
            if year < 1878:
                continue
        except:
            continue
    year_released = "NULL" if pd.isna(movies['title_year'][rows]) else movies['title_year'][rows]
    avg_rating = movies['imdb_score'][rows]
    no_user_ratings = 0 if pd.isna(movies['num_user_for_reviews'][rows]) else movies['num_user_for_reviews'][rows]
    no_user_ratings += 0 if pd.isna(movies['num_critic_for_reviews'][rows]) else movies['num_critic_for_reviews'][rows]
    no_critic_ratings = 0
    statement = f"CREATE (a:Movies {{ movie_id: {movie_id}, title: \"{title}\", url: \"{url}\", duration: {duration}, year_released: {year_released}, avg_rating: {avg_rating}, no_user_ratings: {no_user_ratings}, no_critic_ratings: {no_critic_ratings}}});\n"
    # print(statement)
    f.write(statement)

# Bringing Average Rating in the range of 0-5
statement = "MATCH (p:Movies) SET p.avg_rating = p.avg_rating/2;\n"
f.write(statement)

# Constraints on Genres
statement = "CREATE CONSTRAINT genres_key ON (x:Genres) ASSERT (x.name) IS NODE KEY;\n" 
f.write(statement)

# We are creating genre nodes

genres = set()
for x in range(len(movies)):
    list = movies['genres'][x].split("|")
    for z in list:
        genres.add(z)


for name in genres:
    statement = f'CREATE (a:Genres {{ name: "{name}"}});\n'
    f.write(statement)

# Creating relationships between movies and genres

for x in range(len(movies)):
    movie_id=x
    list = movies['genres'][x].split("|")
    for genre in list:
        statement = f'MATCH (a:Movies),(b:Genres) where a.movie_id = {movie_id} and b.name = "{genre}" CREATE (a)-[r:is_genre]->(b) return r;\n'
        f.write(statement)

# Add Constraints in Celebrity 

statement = "CREATE CONSTRAINT celeb_key ON (x:Celebrity) ASSERT (x.id) IS NODE KEY;\n" 
f.write(statement)

statement = "CREATE CONSTRAINT celeb_name_notnull ON (p:Celebrity) ASSERT exists(p.name);\n"
f.write(statement)

# Creating Celebrity nodes

celebrities = [x for x in movies['actor_1_name'].unique() if not(pd.isna(x))]
celebrities.extend([x for x in movies['actor_2_name'].unique() if not(pd.isna(x))])
celebrities.extend([x for x in movies['actor_3_name'].unique() if not(pd.isna(x))])
celebrities.extend([x for x in movies['director_name'].unique() if not(pd.isna(x))])

celebrities = set(celebrities)
x = 0
for name in celebrities:
    id = x
    gender = "Null"
    dob = "Null"
    statement = f'CREATE (a:Celebrity {{ id: {id}, name: "{name}", gender: "{gender}", dob: "{dob}"}});\n'
    f.write(statement)
    x+=1

# Acted in relationship between celebrity and Movies

for x in range(len(movies)):
    movie_id = x
    if(not(pd.isna(movies['actor_1_name'][x]))):
        actor_1_name = movies['actor_1_name'][x]
        statement = f'MATCH (a:Movies),(b:Celebrity) where a.movie_id = {movie_id} and b.name = "{actor_1_name}" CREATE (b)-[r:acted_in]->(a) return r;\n'
        f.write(statement)
    if(not(pd.isna(movies['actor_2_name'][x]))):
        actor_2_name = movies['actor_2_name'][x]
        statement = f'MATCH (a:Movies),(b:Celebrity) where a.movie_id = {movie_id} and b.name = "{actor_2_name}" CREATE (b)-[r:acted_in]->(a) return r;\n'
        f.write(statement)
    if(not(pd.isna(movies['actor_3_name'][x]))):
        actor_3_name = movies['actor_3_name'][x]
        statement = f'MATCH (a:Movies),(b:Celebrity) where a.movie_id = {movie_id} and b.name = "{actor_3_name}" CREATE (b)-[r:acted_in]->(a) return r;\n'
        f.write(statement)
    if(not(pd.isna(movies['director_name'][x]))):
        director_name = movies['director_name'][x]
        statement = f'MATCH (a:Movies),(b:Celebrity) where a.movie_id = {movie_id} and b.name = "{director_name}" CREATE (b)-[r:directed]->(a) return r;\n'
        f.write(statement)
    
# Constraints on Users

statement = "CREATE CONSTRAINT user_key ON (x:User) ASSERT (x.username) IS NODE KEY;\n" 
f.write(statement)

statement = "CREATE CONSTRAINT user_name_notnull ON (p:User) ASSERT exists(p.name);\n"
f.write(statement)

# Constraints on Critics

statement = "CREATE CONSTRAINT critic_key ON (x:Critic) ASSERT (x.username) IS NODE KEY;\n" 
f.write(statement)

statement = "CREATE CONSTRAINT critic_name_notnull ON (p:Critic) ASSERT exists(p.name);\n"
f.write(statement)

# Constraints on Admin

statement = "CREATE CONSTRAINT admin_key ON (x:Admin) ASSERT (x.username) IS NODE KEY;\n" 
f.write(statement)

statement = "CREATE CONSTRAINT admin_name_notnull ON (p:Admin) ASSERT exists(p.name);\n"
f.write(statement)

# Initialize all relationships
f.write("CREATE ()-[:friend]->();\n")
f.write("CREATE ()-[:request]->();\n")
f.write("CREATE ()-[:likedGenre]->();\n")
f.write("CREATE ()-[:favorite]->();\n")
f.write("CREATE ()-[:rated]->();\n")
f.write("CREATE ()-[:recommended]->();\n")
f.write("CREATE ()-[:review]->();\n")
f.write("CREATE ()-[:recommending_user]->();\n")
f.write("CREATE ()-[:to_whom_recommended]->();\n")
f.write("CREATE ()-[:movie_recommended]->();\n")

# CREATING INDEX
f.write("CREATE INDEX celeb_index FOR (c:Celebrity) ON (c.name);\n")

# Removing unnecessary movies
f.write('MATCH (m:Movies) WHERE m.title contains "Dekalog" detach delete m;\n') 


