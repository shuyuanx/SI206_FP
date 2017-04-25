PROJECT OPTION:
  option 2.

INTRODUCTION:
  In general, the program is getting data from api for OMDb and Twitter, gather the   information, process data, and then output the results of processing data to the output file. User can use it to get data about the movies and directors they are interested for. The program doesn’t require input. However, users can change the movies they want to search for by appending the movie name in the list variable “movie_names” in main function. The output of the program is a text file with information about the movies and twitter data about the directors of the movies. It creates a database with three tables: Movies, Tweets, and Users. Those tables contain information about movies, tweets, and users respectively. 

  The program outputs an output file “206_fp_output.txt,” and caches all data retrieved in a cache file “206_final_project_cache.json.” The program generates a database file called “movies_twitters.db.”

 The program has two classes. Class movie contains information about movies. An instance of Movie represents one movie we are testing about. Class Tweet contains information about the tweets of one query phrase. An instance of Tweet represents all information about one certain query phrase. For example, information about one director, and the director’s name in this case is the query word. 

RUNNING INSTRUCTION:
  run the file called “206_final_project.py”
  terminal input: python 206_final_project.py 

DEPENDENCIES:
  Modules used in this program(Please install before running):
    •unittest
    •tweepy
    •requests
    •json
    •sqlite3
    •collections
    •re

  Files needed to get data from twitter API:
    •“twitter_info.py”: a twitter authentication file. It should include consumer_key, consumer_secret, access_token, access_token_secret.
  
FILES NEEDED:
  none
  No additional files needs to be included for this program to run, except the modules and “twitter_info.py” mentioned above

FUNCTIONS:
  •Name:  get_movie_data
   Input:  Required:  a string: movie_name that the user wants to search about
           Optional:  none
   Return Value:  dictionary movie_data that contains about the movie in the input
   Behavior:  The function takes in a string of a movie name that the user wants to search about, and use OMDb’s api to get information about the movie. Information include title, directors, actors, released date, writes, languages, etc. All data are cached in the cached file. A dictionary containing those information are returned by the function.

  •Name:  get_data_from_twitter
   Input:  Required:  string word that is the query to be searched in the API.
           Optional:  none
   Return Value:  dictionary twitter_data that contains information about the tweets related to the query in the input
   Behavior: The function takes in a query word to search in the twitter’s API and get tweets information. Information include poster screen name, poster id, tweet text, tweet favorite counts, tweet retweeted counts, etc. Data are retrieved by api.search(). All data are cached in the cached file. A dictionary containing all tweets information are returned by the function. 

  •Name:  get_user_data
   Input:  Required:  string username_in, the account the user wants to know about 
           Optional:  none
   Return Value:  dictionary twitter_data that contains information about the user in the input
   Behavior: The function takes in a word username, which the user wants to get information for. It uses api.get_user() function to get data about the users. Information includes user id, user screen name, user description, etc. All data are cached in the cached file. A dictionary containing all users information are returned.

  •Name:  main
   Input:  none 
   Return Value:  none
   Behavior:  All instantiations of objects, all calls of functions, and data processing, output for files happen in main function. 




 