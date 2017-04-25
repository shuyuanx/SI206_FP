import unittest
import tweepy
import requests
import json
import twitter_info 
import sqlite3
import collections
import re

# AUTHENTICATION SETTING:
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
	cache_file.close()
except:
	CACHE_DICTION = {}

# FUNCTION DEFINITIONS:
# get movie data from api

# the base url for movie OMDb
base_url = "http://www.omdbapi.com/?t=";

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
		f.close()

	return movie_data

#get tweets about the query word from twiter api
def get_data_from_twitter(word):
	unique_key = "twitter_query_" + word

	if unique_key in CACHE_DICTION:
		twitter_data = CACHE_DICTION[unique_key]

	else:
		twitter_data = api.search(q = word)
		# but also, save in the dictionary to cache it!
		CACHE_DICTION[unique_key] = twitter_data # add it to the dictionary -- new key-val pair
		# and then write the whole cache dictionary, now with new info added, to the file, so it'll be there even after your program closes!
		f = open(CACHE_FNAME,'w') # open the cache file for writing
		f.write(json.dumps(CACHE_DICTION)) # make the whole dictionary holding data and unique identifiers into a json-formatted string, and write that wholllle string to a file so you'll have it next time!
		f.close()

	return twitter_data

#get twitter information about a twitter user from twitter api
def get_user_data(username_in):
	unique_key = "twitter_user_" + username_in

	if unique_key in CACHE_DICTION:
		twitter_data = CACHE_DICTION[unique_key]

	else:
		twitter_data = api.get_user(username_in)  
		# but also, save in the dictionary to cache it!
		CACHE_DICTION[unique_key] = twitter_data # add it to the dictionary -- new key-val pair
		# and then write the whole cache dictionary, now with new info added, to the file, so it'll be there even after your program closes!
		f = open(CACHE_FNAME,'w') # open the cache file for writing
		f.write(json.dumps(CACHE_DICTION)) # make the whole dictionary holding data and unique identifiers into a json-formatted string, and write that wholllle string to a file so you'll have it next time!
		f.close()

	return twitter_data


# CLASSES DEFINITIONS:
# class Movie represents movie data
class Movie(object):
	#at least 3 instance variables and at least 2 methods besides the constructor. 1 of them could be __str__.
	#ctor accepts a dic that represents a movie.
	#save the neccessray data for a movie: title, director, IMDB rating, a list of actors, number of languages, other information
	
	def __init__(self, movie_in):
		self.title = movie_in["Title"]
		#this is a string
		self.imdbID = movie_in["imdbID"]
		self.actors = movie_in["Actors"]
		self.directors = movie_in["Director"]
		self.writer = movie_in["Writer"]
		self.released = movie_in["Released"]
		self.language = movie_in["Language"]
		self.rating = movie_in["imdbRating"]

	def get_list_of_actors(self):
		actors_list = self.actors.split(",")
		return actors_list

	def get_num_languages(self):
		languages = self.language.split(",")
		return len(languages)

	def get_list_of_directors(self):
		directors_list = self.directors.split(",")
		return directors_list

	def get_top_actor(self):
		actors_list = self.actors.split(",")
		return actors_list[0]

	def get_director(self):
		return self.director

	def __str__(self):
		return "The movie named {} is released in {}, directed by {}. Actors include {}, and the writer is {}. The language of the movie is {}. It is rated {} by IMDB.".format(self.title, self.director, self.actors, self.writer, self.language, self.rating)

#class Tweet represent tweets about the word query(in this program, the directors)
class Tweet(object):
	#define later: needs to represent twitter info for a user. I would search the directors for the movies, so this class will represent the tweets written by directors. 
	def __init__(self, username_in, from_movie, from_movie_id):
		self.username = username_in
		self.movie = from_movie
		self.movie_id = from_movie_id

	def get_info(self):
		self.info = get_data_from_twitter(self.username)
		return self.info

	def __str__(self):
		return "The person's name is {}.".format(self.username)


# MAIN FUNCTION:
# all the initializations and data processing happen in main function
def main():
	#can be deleted later
	print("Main function runs")

	#start with a list of string of movie names: 6 movies in total
	movie_names = []
	movie_names.append("Avatar")
	movie_names.append("The Day After Tomorrow")
	movie_names.append("Forrest Gump")
	movie_names.append("Titanic")
	movie_names.append("Ghost")
	movie_names.append("Frozen")
	movie_names.append("Zootopia")

	#call the get_movie_data function to get info about the movies in the list
	movie_data_results = []
	for name in movie_names:
		movie_data_results.append(get_movie_data(name))

	#create instances of class movie that represents movies in the list 
	#store the instances in movie_instances list
	movie_instances = []
	for data in movie_data_results:
		movie_instances.append(Movie(data))

	#create instances of class tweet that represents the tweet about all directors in all movies
	tweet_class_instances = []
	#get all movies
	for movie in movie_instances:
		#get all directors when there are more than one director for a movie
		directors = movie.get_list_of_directors()
		for director in directors:
			#create the tweet object and store the object in the list
			a_tweet_class = Tweet(director, movie.title, movie.imdbID)
			tweet_class_instances.append(a_tweet_class)

	# TABLE DEFINITIONS AND INITIALIZATIONS:
	# Make a connection to a new database movies_twitters.db
	conn = sqlite3.connect('movies_twitters.db') 
	cur = conn.cursor()

	# table Movies for movies and input the data into the table
	cur.execute('DROP TABLE IF EXISTS Movies')

	table_spec = 'CREATE TABLE IF NOT EXISTS '
	table_spec += 'Movies (id TEXT PRIMARY KEY, ' 
	table_spec += 'title TEXT, ' 
	table_spec += 'director TEXT, ' 
	table_spec += 'num_languages TEXT, '
	table_spec += 'languages TEXT, ' 
	table_spec += 'IMDB_rating TEXT, ' 
	table_spec += 'top_actor TEXT, ' 
	table_spec += 'released TEXT, ' 
	table_spec += 'writer TEXT)' 
	
	cur.execute(table_spec)
	conn.commit()

	#insert the data for movie in the list into the table Movies database
	statement = 'INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'

	#for each movie, store all the required data and some more data
	for movie in movie_instances:
		movie_data = []
		movie_data.append(movie.imdbID)
		movie_data.append(movie.title)
		movie_data.append(movie.directors)
		movie_data.append(movie.get_num_languages())
		movie_data.append(movie.language)
		movie_data.append(movie.rating)
		movie_data.append(movie.get_top_actor())
		movie_data.append(movie.released)
		movie_data.append(movie.writer)

		cur.execute(statement, movie_data)

	conn.commit()


	# table Tweets for tweets
	cur.execute('DROP TABLE IF EXISTS Tweets')

	table_spec = 'CREATE TABLE IF NOT EXISTS '
	table_spec += 'Tweets (tweet_id INTEGER PRIMARY KEY, '
	table_spec += 'tweet_text TEXT, '  

	table_spec += 'from_movie TEXT, ' 
	table_spec += 'from_movie_id TEXT, ' 
	table_spec += 'num_fav INTEGER, ' 
	table_spec += 'num_ret INTEGER, ' 
	table_spec += 'poster TEXT, ' 
	table_spec += 'poster_id TEXT, ' 
	table_spec += 'FOREIGN KEY(poster_id) REFERENCES Movies(id))'
	
	cur.execute(table_spec)

	statement = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?, ?, ?, ?)'

	#all_users contains all the user names that posted the tweets that we retrieve and all the users mentioned in those. All the nerghbors in the social network
	all_users = []
	#all_tweet_id contains all the id numbers for all tweets we retrieve.
	all_tweet_id = []

	#for each tweet, store all required information and more interesting information
	for a_tweet in tweet_class_instances:
		tweetinfo = a_tweet.get_info()
		for tweet in tweetinfo["statuses"]:
			if tweet["id"] not in all_tweet_id: 
				tweet_info = []
				#print(json.dumps(tweet, indent = 4))
				tweet_info.append(tweet["id"])
				all_tweet_id.append(tweet["id"])
				tweet_info.append(tweet["text"])
				#have both the movie's name and the id(the primary key for table Movies)
				tweet_info.append(a_tweet.movie) 
				tweet_info.append(a_tweet.movie_id)
				tweet_info.append(tweet["favorite_count"])
				tweet_info.append(tweet["retweet_count"])
				#have both the user's name and the id(the primary key for table Users)
				tweet_info.append(tweet["user"]["screen_name"])
				tweet_info.append(tweet["user"]["id"])

				#add all the posters
				all_users.append(tweet["user"]["screen_name"]) 
				#add all users mentioned in the tweet
				for user in tweet["entities"]["user_mentions"]: 
					all_users.append(user["screen_name"])

				cur.execute(statement, tweet_info)

	conn.commit()

	#set up table Users
	cur.execute('DROP TABLE IF EXISTS Users')

	table_spec = 'CREATE TABLE IF NOT EXISTS '
	table_spec += 'Users (user_id TEXT PRIMARY KEY, '
	table_spec += 'screen_name TEXT, '  
	table_spec += 'num_fav INTEGER, ' 
	table_spec += 'description TEXT)' 
	 
	cur.execute(table_spec)

	statement = 'INSERT INTO Users VALUES (?, ?, ?, ?)'

	#all_users set has no duplicates, to ensure that users won't be inserted to table twice(that violates the primary key unique constraint)
	all_users = set(all_users)
	#all_users_twitter is the list of User-representative dictionaries
	all_users_twitter = []

	for user in all_users:
		user_result = get_user_data(user)
		all_users_twitter.append(user_result)

	#for every user's information stored in all_user_twitter, parse the data, and store the information into the table
	for user_result in all_users_twitter:
		user_info = []
		user_info.append(user_result["id"])
		user_info.append(user_result["screen_name"])
		user_info.append(user_result["favourites_count"])
		user_info.append(user_result["description"])

		cur.execute(statement, user_info)
	
	#commit to save the changes to database
	conn.commit()

	# QUERIES:
	# FIRST QUERY:
	# get all tweets from users who have more than 5000 favorite counts and store the list of results in tweets_from_popular_poster
	query = "SELECT poster, tweet_text, from_movie, Users.description FROM Tweets INNER JOIN Users on Tweets.poster_id=Users.user_id WHERE Users.num_fav > 5000" 
	cur.execute(query)
	tweets_from_popular_poster = cur.fetchall()

	#LIST COMPREHENSION to get screen names of all popular posters(those who have more than 5000 favorite counts). Store the list of screen names in popular_posters
	popular_posters = [
		one[0] 
		for one in tweets_from_popular_poster
		if len(one[0]) > 2
	] 

	# SECOND QUERY
	# get all movies about which tweets are retweeted more than or equal to 3 times. Store a list of the movies in movies_with_retweeted_tweets
	query = "SELECT title, top_actor, num_languages, languages, Tweets.num_ret FROM Movies INNER JOIN Tweets on Tweets.from_movie_id=Movies.id WHERE Tweets.num_ret >= 3" 
	cur.execute(query)
	movies_with_retweeted_tweets = cur.fetchall() 

	# USE THE BUILT-IN MAP AND LAMBDA FUNCTION
	# get the data from movies and tweets and return a list of string for future reference when outputing data
	movie_languages = map(lambda x: "Movie {} has {} language(s): {}.".format(x[0], x[2], x[3]), movies_with_retweeted_tweets)

	#make it a unique set
	movie_languages = set(movie_languages)
	#the way to print it to screen
	# for one in movie_languages:
	# 	print(type(one))
	# 	print(one)

	# THIRD QUERY
	query = "SELECT tweet_text FROM Tweets"
	cur.execute(query)
	movie_tweets = cur.fetchall()

	# SET COMPREHENSION to generate a list of all tweet texts
	all_tweet_text = {
		movie[0]
		for movie in movie_tweets
	}

	# USE REGULAR EXPRESSION AND RE
	# get all retweeted tweets for future output
	regex_result = []

	for text in all_tweet_text:
		regex = r"RT .*: (.*)"
		#print(text)
		result = re.match(regex, text)
		regex_result.append(result)

	#the way to output it to screen
	# for regex in regex_result:
	# 	if regex is not None:
	# 		print(regex.group(1))

	# FOURTH QUERY
	# get movies about which tweets have more than 0 favorite counts
	query = "SELECT title, Tweets.tweet_text FROM Movies INNER JOIN Tweets on Tweets.from_movie_id=Movies.id WHERE num_fav > 0"
	cur.execute(query)
	movies_with_favorite_tweets = cur.fetchall() 

	# USE COLLECTION 
	# USE DICTIONARY ACCUMULATION
	# USE SORT BY PARAMETER
	# for all the tweets, gather the together by movie title. Store the all the tweet texts and the corresponding movie title inthe diction_listvals
	diction_listvals = collections.defaultdict(list)
	for k, v in movies_with_favorite_tweets:
		diction_listvals[k].append(v)
	#sort by the movie title name and then print out
	diction_listvals = sorted(diction_listvals.items())

	#remember to close the connection to the database file after done with modifying and getting data from database to avoid unexpected results
	conn.close()

	# OUTPUT:
	OUTPUT_FILE = "206_fp_output.txt"
	f = open(OUTPUT_FILE, 'w')

	# print all movie names
	for movie in movie_names:
		f.write(movie)
		f.write(", ")

	#print the summary and date
	f.write("Twitter summary on April 25th, 2017. \n\n")

	# FIRST QUERY OUTPUT:
	# print the most popular posters
	f.write("Popular twitter posters(who have more than 5000 favorite counts) that posted about directors of movies in the list: \n")
	for poster in popular_posters:
		f.write(poster)
		f.write("\n")

	# SECOND QUERY OUTPUT:
	# print the languages that the movie has
	f.write("\n")
	f.write("Movies of the directors that are tweeted about and retweeted a lot on twitter and the languages they have: \n")
	for one in movie_languages:
		f.write(one)
		f.write("\n")


	# THIRD QUERY OUTPUT:
	f.write("\n")
	f.write("The text of the retweeted tweets among the tweets about the directors of the movies in the list: \n")
	for regex in regex_result:
			if regex is not None:
				f.write(regex.group(1))
				f.write("\n")

	# FOURTH QUERY OUTPUT:
	f.write("\n")
	f.write("Tweets searched by directors names grouped by the movie's title: \n")
	i = 1;
	for movie in diction_listvals:
		f.write("The movie ")
		print(movie[0])
		f.write(movie[0])
		f.write(" has the tweets: ")
		for tweet in movie[1]:
			f.write("TWEET ")
			f.write(str(i))
			f.write(": \n")
			f.write(tweet)
			f.write("\n")
			f.write("\n")
			i += 1

	# close it after all outputs are done
	f.close()


# TEST CASES:
# have at least 1 test for each function
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



# INVOKE MAIN FUNCTION:
if __name__ == "__main__":
	main()

# INVOKE TEST CASES
#unittest.main(verbosity=2) 


#output to file
#test cases
#documentation
#wrap it up
