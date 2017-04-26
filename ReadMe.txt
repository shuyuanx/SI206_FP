PROJECT OPTION:
  option 2.

INTRODUCTION:
  In general, the program is getting data from api for OMDb and Twitter, gather the   information, process data, and then output the results of processing data to the output file. User can use it to get data about the movies and directors they are interested for. The program doesn’t require input. However, users can change the movies they want to search for by appending the movie name in the list variable “movie_names” in main function. The output of the program is a text file with information about the movies and twitter data about the directors of the movies. It creates a database with three tables: Movies, Tweets, and Users. Those tables contain information about movies, tweets, and users respectively. 

 The program has two classes. Class movie contains information about movies. An instance of Movie represents one movie we are testing about. Class Tweet contains information about the tweets of one query phrase. An instance of Tweet represents all information about one certain query phrase. For example, information about one director, and the director’s name in this case is the query word. 

RUNNING INSTRUCTION:
  run the file called “206_final_project.py”
  terminal input: python 206_final_project.py 
  Notice: Since the tweets retrieved may have special characters, the output file may have special characters. Not all applications on all computers work for the text file. It would be better to use Sublime Text Editor or Chrome to open the output text file if possible.

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
  
FILES INCLUDED:
  No additional files need to be included for this program to run, except the modules and “twitter_info.py” mentioned above.

  The program generates:
     •“206_fp_output.txt”: contains all the output
     •“206_final_project_cache.json”: contains all the cached data retrieved from API
     •“movies_twitters.db”: contains three tables

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

CLASSES:
  •Name:  Movie
   Instance:  an instance represents one movie. It contains all the data like directors, actors, writers in the instance variables. 
   Ctor input:  dictionary movie_in, which contains all the data about the movie. 
   Method:
     •name:  get_list_of_actors
      input:  none
      behavior:  retrieves the string variable actor in the class. It splits the string into list by “,” and returns the list.   
      return value:  list actors_list that contains all actor names as strings

     •name:  get_num_languages
      input:  none
      behavior:  retrieves the string variable language in the class. It splits the string into list by “,” and returns the length list 
      return value:  int length of the language list

     •name:  get_list_of_directors
      input:  none
      behavior:  retrieves the string variable directors in the class. It splits the string into list by “,” and returns the list. 
      return value:  list directors_list that contains all directors names as string variables 

     •name:  get_top_actor
      input:  none
      behavior:  retrieves the string variable actor in the class. It splits the string into list by “,” and returns the first element in the list
      return value:  string variable contains the first actor for the movie

	•name:  __str__ (print function)
      input:  none
      behavior:  prints the movie object in format when print() function is called
      return value:  a string in a certain format

  •Name:  Tweet
   Instance:  an instance represent all tweets retrieved for one query word (in this case, the director’s name). It contains all information including poster of tweets, tweet text, etc.  
   Ctor input:  string query word(the director’s name), string movie title that the director directs, string movie id 
   Method:
     •name: get_info
      input:  none
      behavior:  calls the get_data_from_twittter() function defined above, on the query word(director’s name), and stores the data in the instance variable self.info. Returns the dictionary.
      return value:  dictionary that contains information about the tweets about the directory

     •name: __str__ (print function)
      input:  none
      behavior:  prints the tweet object in certain format
      return value:  a string that contains information about tweet object in certain format

DATABASE:
  TABLE Movies:
    •id: Primary Key
         The unique id number from the OMBd database for the movie. (text)
    •title:  the title of the movie (text)
    •director:  the director(s) for the movie (text)
    •num_languages:  the number of languages that the movie has (text)
    •language:  the names of the languages the movies has (text)
    •IMDB_Rating:  the rating on the IMDb database for the movie (text)
    •top_actor:  the first actor in the list for the movie (text)
    •released:  the date released (text)
    •writer:  the writer(s) of the movie (text)

  TABLE Tweets:
    •tweet_id:  Primary Key
                The unique id number for the tweet on twitter (int)
    •tweet_text:  the content of the tweet (text)
    •from_movie:  which movie the tweet’s director directs (text)
    •from_movie_id:  the unique id number of the movie(text)
    •num_fav:  how many people favorite this tweet (int)
    •num_ret:  how many people retweet this tweet (int)
    •poster:  the poster of the tweet’s screen name (text)
    •poster_id:  Reference to the Users Table
                 the poster’s unique id 

  TABLE Users:
    •user_id:  Primary Key
               The unique id number for the user on twitter (text)
    •screen_name:  the screen name of the user on twitter (text)
    •num_fav:  how many people favorite this user (int)
    •description:  a short description about the user in text (text)

DATA MANIPULATION:
  First Query:
  The program find all posters who posted tweets that mentioned the directors of the movies in the list, and among those who are popular (favorited by more than 5000 people). The program outputs this information in the output file, and it helps user know who likes to talk about the movies. 

  Second Query:
  The program finds tweets that are tweeted more than or equal to 3 times, and it gets the movies that the director related to the tweets directs and outputs the title of the movie, the number of languages of the movie, and what those languages are to the output file. It is useful for people who are interested in watching the movie to check if there is a version that’s in their language. 

  Third Query:
  Among all tweets that are retweeted more than favorited, it finds tweets that are retweeted from others, and get ride of the RT prefix of the tweets. It shows only the contents of the retweeted tweets on the output file. This information informs users the popular topics about the directors and the movies.

  Fourth Query:
  It filters all tweets that have more than 0 favorites. It groups all tweets that satisfies the requirement into groups by the movie that the director(which the tweets is about) directs. The user is able to see all tweets related to each movie that has ever been favorited. This helps the user know more information about the movies, and it’s particular useful because it filters out the tweets that people don’t think are useful or interesting.   
 
REASONS FOR CHOOSING THE PROJECT:
  This project seems interesting, because I will get data from two different databases, and gather the information together to make them make sense. I will get data about the intersection, and use data retrieved from one database to search for more data in the second database. It is very practical, and the same technique can be applied to many applications in the future. I am also interested in the OBDb database.  

SPECIFIC NOTES FOR SI_206:
Line(s) on which each of your data gathering functions begin(s):
  •38: get_movie_data()
  •59: get_data_from_twitter()
  •77: get_user_data()

Line(s) on which your class definition(s) begin(s):
  •97: class Movie
  •133: class Tweet

Line(s) where your database is created in the program:
  •202: created database file “movies_twitters.db”

Line(s) of code that load data into your database:
  •206: load into Movies
  •244: load into Tweets
  •297: load into Users

Line(s) of code (approx) where your data processing code occurs — where in the file can we see all the processing techniques you used?
  •334: queries begin. There are 4 queries in total. Comments indicate the start and end of each query.

Line(s) of code that generate the output.
  •408: output begins. Output for 4 queries are indicated by comments.

OK to be approximate here — ok if it ends up off by 1 or 2. Make it easy for us to find!