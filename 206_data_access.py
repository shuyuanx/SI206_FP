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
def get_data_from_twitter(username):
	unique_key = "twitter_user_" + username

	if unique_key in CACHE_DICTION:
		twitter_data = CACHE_DICTION[unique_key]

	else:
		twitter_data = api.user_timeline(username)
		# but also, save in the dictionary to cache it!
		CACHE_DICTION[unique_key] = twitter_data # add it to the dictionary -- new key-val pair
		# and then write the whole cache dictionary, now with new info added, to the file, so it'll be there even after your program closes!
		f = open(CACHE_FNAME,'w') # open the cache file for writing
		f.write(json.dumps(CACHE_DICTION)) # make the whole dictionary holding data and unique identifiers into a json-formatted string, and write that wholllle string to a file so you'll have it next time!
		f.close()

	return twitter_data

class Movie(object):
	#at least 3 instance variables and at least 2 methods besides the constructor. 1 of them could be __str__.
	#ctor accepts a dic that represents a movie.
	#save the neccessray data for a movie: title, director, IMDB rating, a list of actors, number of languages, other information
	
	def __init__(self, movie_in):
		self.title = movie_in["Title"]
		#this is a string
		self.actors = movie_in["Actors"]
		self.director = movie_in["Director"]
		self.writer = movie_in["Writer"]
		self.released = movie_in["Released"]
		self.language = movie_in["Language"]
		self.rating = movie_in["imdbRating"]

	def get_list_of_actors(self):
		actors_list = self.actors.split(",")
		return actors_list

	def __str__(self):
		return "The movie named {} is released in {}, directed by {}. Actors include {}, and the writer is {}. The language of the movie is {}. It is rated {} by IMDB.".format(self.title, self.director, self.actors, self.writer, self.language, self.rating)

#this is what the result for get movie data should look like. Only showing it here for reference. And it's just used for testing for now. It will be changed it later, and won't be hardcoded in function or classes.
movie_ghost = {"Title":"Ghost","Year":"1990","Rated":"PG-13","Released":"13 Jul 1990","Runtime":"127 min","Genre":"Drama, Fantasy, Romance","Director":"Jerry Zucker","Writer":"Bruce Joel Rubin","Actors":"Patrick Swayze, Demi Moore, Whoopi Goldberg, Tony Goldwyn","Plot":"After a young man is murdered, his spirit stays behind to warn his lover of impending danger, with the help of a reluctant psychic.","Language":"English","Country":"USA","Awards":"Won 2 Oscars. Another 16 wins & 22 nominations.","Poster":"https://images-na.ssl-images-amazon.com/images/M/MV5BMTU0NzQzODUzNl5BMl5BanBnXkFtZTgwMjc5NTYxMTE@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"7.0/10"},{"Source":"Rotten Tomatoes","Value":"74%"},{"Source":"Metacritic","Value":"52/100"}],"Metascore":"52","imdbRating":"7.0","imdbVotes":"160,136","imdbID":"tt0099653","Type":"movie","DVD":"24 Apr 2001","BoxOffice":"N/A","Production":"Paramount Pictures","Website":"N/A","Response":"True"}


#class Tweet(object):



#write the main function: write the class instantiation and function calls in main. The process of actually obtaining and parsing data should go in main here. 

#def main():

#call the get_movie_data functions to get info about the movie ghost
movie1_data = get_movie_data("ghost")
print(movie1_data);

#create an instance of class movie that represents the movie ghost
movie1 = Movie(movie1_data)

#call get data from twitter
#get the tweets from the director of the first movie ghost
twitter_result1 = get_data_from_twitter(movie1.director)
print(type(twitter_result1))
print(twitter_result1)

#set up a table and input the data into the table
# Make a connection to a new database tweets.db, and create a variable to hold the database cursor.
conn = sqlite3.connect('movies_twitters.db') 
cur = conn.cursor()

# Write code to drop the Tweets table if it exists, and create the table (so you can run the program over and over), with the correct (4) column names and appropriate types for each.
# HINT: Remember that the time_posted column should be the TIMESTAMP data type!
cur.execute('DROP TABLE IF EXISTS Movies')

table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'movies (movie_id INTEGER PRIMARY KEY, ' 
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

#just one movie for now, but more movies will be added. So a loop will be used
movie_data = []
#in the future loop, a int count will be initialized and increased in each iteration.
#this int will be the primary key and id for the movie in the database
movie_data.append(0)
movie_data.append(movie1.writer)
movie_data.append(movie1.actors)
movie_data.append(movie1.released)
movie_data.append(movie1.language)
movie_data.append(movie1.rating)
movie_data.append(movie1.director)

print(movie_data)

cur.execute(statement, movie_data)


#create three instances of class Movie using the data obtained above

#instantiate the class Tweet to get data from twitter here

#if __name__ == "__main__":
	#main()


# Write your test cases here.
# Those tests will be modifies
# Modify these tests and add more teste later. Need to test the functions and the classes as well.
class test_class_Movie(unittest.TestCase):
	def test_class_ctor(self):
		movie1 = Movie({movie_ghost})
		self.assertEqual(type(movie1.director, type("abs")))

	def test_get_writer(self):
		movie1 = Movie({movie_ghost})
		self.assertEqual(type(movie1.get_list_of_actors(), type(["a","b"])))

	def test_get_actors(self):
		movie1 = Movie({movie_ghost})
		self.assertEqual(type(movie1.actors), type("actors"))

	def test_process_data(self):
		movie1 = Movie({movie_ghost})
		self.assertEqual(type(movie1.released), type("actors"))

class class_Twitter(unittest.TestCase):
	def test_article_ctor(self):
		list = []
		article1 = Article(text_from_site)
		self.assertEqual(type(article1.authors), type(list))

	def test_get_author(self):
		article1 = Article(text_from_site)
		string = ""
		self.assertEqual(type(article1.get_author()), type(string))

	def test_get_description(slef):
	    string = ""
	    article1 = Article(text_from_site)
	    self.assertEqual(type(article1.get_description()), type(string))

class class_Authors(unittest.TestCase):
	def test_author_ctor(self):
		list = []
		author1 = Author(text_from_site)
		assertEqual(type(list), type(author1.articles))

	def	test_get_article(self):
		author1 = Author(text_from_site)
		list = []
		assertEqual(type(list), type(author1.articles))

	def test_get_article_number(self):
		author1 = Author(text_from_site)
		number = 0;
		assertEqual(type(number), type(author1.get_article_number()))

## Remember to invoke all your tests...
##unittest.main(verbosity=2) 