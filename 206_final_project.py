import unittest
import tweepy
import requests
import json
import twitter_info 
import sqlite3

# Information stored in twitter_info.py file
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret

#set up the authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

#caching data and try to get data from chached file
CACHE_FNAME = "206_final_project_cache.json"
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

#the base url for movie OMDb
base_url = "http://www.omdbapi.com/?t=";

#function writting starts here
def get_movie_data(movie_name):
	unique_key = "movie_" + movie_name

	if unique_key in CACHE_DICTION:
		movie_data = CACHE_DICTION[unique_key]

	else:
		url = base_url + movie_name
		#this is a string
		movie_string = requests.get(url).text
		movie_data = json.loads(movie_string)

		#catch the data in file
		CACHE_DICTION[unique_key] = movie_data 
		f = open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close

	return movie_data

#write a function to get data from twitter
def get_data_from_twitter(username_in):
	unique_key = "twitter_user_" + username_in

	if unique_key in CACHE_DICTION:
		twitter_data = CACHE_DICTION[unique_key]

	else:
		twitter_data = api.search(q = username_in)
		# but also, save in the dictionary to cache it!
		CACHE_DICTION[unique_key] = twitter_data # add it to the dictionary -- new key-val pair
		# and then write the whole cache dictionary, now with new info added, to the file, so it'll be there even after your program closes!
		f = open(CACHE_FNAME,'w') # open the cache file for writing
		f.write(json.dumps(CACHE_DICTION)) # make the whole dictionary holding data and unique identifiers into a json-formatted string, and write that wholllle string to a file so you'll have it next time!
		f.close()

		print(type(twitter_data))

	return twitter_data


#classes
class Movie(object):
	#at least 3 instance variables and at least 2 methods besides the constructor. 1 of them could be __str__.
	#ctor accepts a dic that represents a movie.
	#save the neccessray data for a movie: title, director, IMDB rating, a list of actors, number of languages, other information
	
	def __init__(self, movie_in):
		self.title = movie_in["Title"]
		#this is a string
		self.actors = movie_in["Actors"]
		self.directors = movie_in["Director"]
		self.writer = movie_in["Writer"]
		self.released = movie_in["Released"]
		self.language = movie_in["Language"]
		self.rating = movie_in["imdbRating"]

	def get_list_of_actors(self):
		actors_list = self.actors.split(",")
		return actors_list

	def get_list_of_directors(self):
		directors_list = self.directors.split(",")
		return directors_list

	def get_director(self):
		return self.director

	def __str__(self):
		return "The movie named {} is released in {}, directed by {}. Actors include {}, and the writer is {}. The language of the movie is {}. It is rated {} by IMDB.".format(self.title, self.director, self.actors, self.writer, self.language, self.rating)


class Tweet(object):
	#define later: needs to represent twitter info for a user. I would search the directors for the movies, so this class will represent the tweets written by directors. 
	def __init__(self, name_in):
		self.name = name_in
		self.text = ""

	def get_info(self):
		self.info = get_data_from_twitter(name)
		return self.info

	def parse_data(self):
		self.text = self.info["statuses"][10]["text"]

	def __str__(self):
		return "The person's name is {}.".format(self.name)






#write the main function: write the class instantiation and function calls in main. The process of actually obtaining and parsing data should go in main here. 

#def main():

#a list of string of movie names
movie_names = []
movie_names.append("ghost")
movie_names.append("titanic")
movie_names.append("Forrest Gump")
movie_names.append("Zootopia")


#call the get_movie_data functions to get info about the movie ghost
movie_data_results = []

for name in movie_names:
	movie_data_results.append(get_movie_data(name))


#create instances of class movie that represents the movie ghost 
#store the instances in movie_instances list
movie_instances = []
for data in movie_data_results:
	movie_instances.append(Movie(data))


one_director = movie_instances[0].get_list_of_directors()[0]
tweet = Tweet(one_director)
print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
tweet.get_info()
tweet.parse_data()
print(tweet.text)

#call get data from twitter
#get the tweets from the director of the first movie ghost
twitter_directors = [];
for movie in movie_instances:
	directors = movie.get_list_of_directors()
	for director in directors:
		twitter_directors.append(get_data_from_twitter(director))
		print(director)


#set up a table Movies for movies and input the data into the table
# Make a connection to a new database tweets.db, and create a variable to hold the database cursor.
conn = sqlite3.connect('movies_twitters.db') 
cur = conn.cursor()


cur.execute('DROP TABLE IF EXISTS Movies')

table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'movies (title TEXT PRIMARY KEY, ' 
table_spec += 'writer TEXT, ' 
table_spec += 'actors TEXT, ' 
table_spec += 'released TEXT, ' 
table_spec += 'language TEXT, ' 
table_spec += 'rating TEXT, ' 
table_spec += 'director TEXT)' 
cur.execute(table_spec)
conn.commit()

#insert the data for movie ghost into the table Movies database
statement = 'INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?, ?)'

#in the future loop, a int count will be initialized and increased in each iteration.
#this int will be the primary key and id for the movie in the database
for movie in movie_instances:
	movie_data = []
	movie_data.append(movie.title)
	movie_data.append(movie.writer)
	movie_data.append(movie.actors)
	movie_data.append(movie.released)
	movie_data.append(movie.language)
	movie_data.append(movie.rating)
	movie_data.append(movie.directors)

	cur.execute(statement, movie_data)

# Set up a table Tweets for tweets
# Write code to drop the Tweets table if it exists, and create the table (so you can run the program over and over), with the correct (4) column names and appropriate types for each.
cur.execute('DROP TABLE IF EXISTS Tweets')

table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Tweets (tweet_id INTEGER PRIMARY KEY, ' 
table_spec += 'author TEXT, ' 
table_spec += 'tweet_text TEXT, ' 
table_spec += 'user_mentioned TEXT, ' 
table_spec += 'retweets INTEGER)' 
cur.execute(table_spec)

statement = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?)'

#add more twitter information to twitters later

# input the data for twitters into the table Tweets



for tweet in twitter_directors:
	print("**************************************")
	print(json.dumps(tweet["statuses"][10], indent=4))
	print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
	print(tweet["statuses"][10]["id"])
	print(tweet["statuses"][10]["text"])
	print(tweet["statuses"][10]["user"]["screen_name"])
	print(tweet["statuses"][10]["user"]["id"])
	for user in tweet["statuses"][0]["entities"]["user_mentions"]:
		print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
		print(json.dumps(user, indent=4))

		print(user["screen_name"])
		print(user["id"])

	print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

	
	

	print(type(tweet))
	print(type(tweet["statuses"]))
	tweet_info = []
	tweet_info.append(tweet["statuses"][0]["id"])
	tweet_info.append(tweet["statuses"][0]["id"])
	tweet_info.append(tweet["statuses"][0]["id"])
	tweet_info.append(tweet["statuses"][0]["id"])
	tweet_info.append(tweet["statuses"][0]["id"])



	tweet_info.append(tweet["user"]["screen_name"])
	tweet_info.append(tweet["created_at"])
	tweet_info.append(tweet["text"])
	tweet_info.append(tweet["retweet_count"])

	cur.execute(statement, tweet_info)

# Use the database connection to commit the changes to the database
conn.commit()

#remember to close the connection to the database file after done with modifying and getting data from database to avoid unexpected results
conn.close()

#make three more calls to the get movie data function



#create three instances of class Movie using the data obtained above


#add more data to the table Movies


#make three more calls to the get data from twitter function


#instantiate the class Tweet to get data from twitter here


#add more data to the table Tweets

#parse twitter data

#create another table

#process data and create an output file

#invoke the main function
#if __name__ == "__main__":
	#main()


# Write more test cases here.
# Those tests will be modifies
# Modify these tests and add more teste later. Need to test the functions and the classes as well.
class test_class_Movie(unittest.TestCase):
	def test_class_ctor(self):
		movie1 = Movie({movie1_data})
		self.assertEqual(type(movie1.director, type("abs")))

	def test_get_writer(self):
		movie1 = Movie({movie1_data})
		self.assertEqual(type(movie1.get_list_of_actors(), type(["a","b"])))

	def test_get_actors(self):
		movie1 = Movie({movie1_data})
		self.assertEqual(type(movie1.actors), type("actors"))

	def test_process_data(self):
		movie1 = Movie({movie1_data})
		self.assertEqual(type(movie1.released), type("actors"))

class class_Twitter(unittest.TestCase):
	def test_twitter(self):
		list = []
		tweet1 = Tweet(text_from_site)
		self.assertEqual(type(tweet1.numLiked), type(123))

	def test_get_text(self):
		string = ""
		tweet1 = Tweet(text_from_site)
		self.assertEqual(type(twee1.get_some_text()), type("sdf"))

	def test_get_description(slef):
		string = ""
		tweet1 = Tweet(text_from_site)
		self.assertEqual(type(tweet1.retweets), type(43))

class class_test_other(unittest.TestCase):
	def test_author(self):
		list = []
		movie1 = Movie({movie1_data})
		assertEqual(type("2"), type(movie1.writer))

	def	test_get_data_twitter(self):
		list = []
		assertEqual(type(list), type(twitter_result1))

	def test_get_movie_data(self):
		dic = {}
		number = 0;
		assertEqual(type(dic), type(movie1_data))

## Remember to invoke all your tests...
#unittest.main(verbosity=2) 