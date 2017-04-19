## Your name: Shuyuan
## The option you've chosen: Option 1

# Put import statements you expect to need here!

import unittest
import requests
from bs4 import BeautifulSoup


cache_filename = "206_final_project_cache.json"
url_for_site = "https://www.nps.gov/index.htm"
text_from_site = ""

try:
	#check if the file exists
	#f = open(cache_filename, 'r')
	text_from_site = r.read()
	f.close()

except:
	#if there is no such file, get the data from the website and save it to a file
	r = requests.get(url_for_site)
	text_from_site = r.text
	f = open(cache_filename, "w")
	#af.write(text_from_site)
	f.close()



soup = BeautifulSoup(text_from_site, 'html.parser')
print(type(soup))

#parks = soup.find_all()
national_parks = []

class NationalPark(object):
    def __init__(self, text_from_site):
        self.text = text_from_site
        self.contact_number = 1
        #list or string to be determined later
       

    #def __str__(self):
    #    return "This is a park, which is located on {}, in {}, with contact number {}"

    #def get_contact_number():

    #def get_street_address():





movie_ghost = {"Title":"Ghost","Year":"1990","Rated":"PG-13","Released":"13 Jul 1990","Runtime":"127 min","Genre":"Drama, Fantasy, Romance","Director":"Jerry Zucker","Writer":"Bruce Joel Rubin","Actors":"Patrick Swayze, Demi Moore, Whoopi Goldberg, Tony Goldwyn","Plot":"After a young man is murdered, his spirit stays behind to warn his lover of impending danger, with the help of a reluctant psychic.","Language":"English","Country":"USA","Awards":"Won 2 Oscars. Another 16 wins & 22 nominations.","Poster":"https://images-na.ssl-images-amazon.com/images/M/MV5BMTU0NzQzODUzNl5BMl5BanBnXkFtZTgwMjc5NTYxMTE@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"7.0/10"},{"Source":"Rotten Tomatoes","Value":"74%"},{"Source":"Metacritic","Value":"52/100"}],"Metascore":"52","imdbRating":"7.0","imdbVotes":"160,136","imdbID":"tt0099653","Type":"movie","DVD":"24 Apr 2001","BoxOffice":"N/A","Production":"Paramount Pictures","Website":"N/A","Response":"True"}

print(type(movie_ghost))


# Write your test cases here.

class class_NationalPark(unittest.TestCase):
	def test_class_ctor(self):
		string = ""
		park1 = NationalPark(text_from_site)
		self.assertEqual(park1.contact_number, 1)

	def test_get_state(self):
		park1 = NationalPark(text_from_site)
		string = ""
		self.assertEqual(type(park1.get_state()), type(string))

	def test_get_street_address(self):
		park1 = NationalPark(text_from_site)
		string = " "
		self.assertEqual(type(park1.get_street_address()), type(string))

	def test_process_data(self):
		park1 = NationalPark(text_from_site)
		string = ""
		self.assertEqual(type(park1.process_data()), type(string))

class class_Articles(unittest.TestCase):
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
unittest.main(verbosity=2) 