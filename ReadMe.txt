PROJECT OPTION:
option 2.

INTRODUCTION:
In general, the program is getting data from api for OMDb and Twitter, gather the information, process data, and then output the results of processing data to the output file. User can use it to get data about the movies and directors they are interested for. The program doesn��t require input. However, users can change the movies they want to search for by appending the movie name in the list variable ��movie_names�� in main function. The output of the program is a text file with information about the movies and twitter data about the directors of the movies. It creates a database with three tables: Movies, Tweets, and Users. Those tables contain information about movies, tweets, and users respectively. 

RUNNING INSTRUCTION:
run the file called ��206_final_project.py��
terminal input: python 206_final_project.py

DEPENDENCIES:
Modules used in this program(Please install before running):
  �6�1unittest
  �6�1tweepy
  �6�1requests
  �6�1json
  �6�1twitter_info 
  �6�1sqlite3
  �6�1collections
  �6�1re

Files needed to get data from twitter API:
your own twitter authentication file, and it should be properly named ��twitter_info.py��. It should include consumer_key, consumer_secret, access_token, access_token_secret.


I have two classes in the program. Class movie contains information about movies. An instance of Movie represents one movie we are testing about. Class Tweet contains information about the tweets of one query phrase. An instance of Tweet represents all information about one certain query phrase. For example, information about one director, and the director��s name in this case is the query word. 