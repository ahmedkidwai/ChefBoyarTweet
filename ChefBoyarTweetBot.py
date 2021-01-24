import nltk
import requests
from recipe_scrapers import scrape_me
from RevImg import RevImg
from textblob import TextBlob
from bs4 import BeautifulSoup
from PIL import Image, ImageFont, ImageDraw
import textwrap

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import time
import twitter_credentials
import json


class StdOutListener(StreamListener):

    def on_data(self, data):
        json_data = json.loads(data)
        # Check if original tweet is a reply (i.e we want to parse an image)
        if json_data['in_reply_to_status_id_str']:
            tweet_user = "@" + json_data['user']['screen_name']
            original_tweet_id = json_data['in_reply_to_status_id_str']
            
        # If we want to get a recipe from a link
        else:

            

        print(data)
        


        return(True)
    def on_error(self, status):
        print(status)


# # # # Global # # # #
auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,
                    twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN,
                      twitter_credentials.ACCESS_TOKEN_SECRET)
api = API(auth, wait_on_rate_limit=True,
          wait_on_rate_limit_notify=True)

def bestImageGuess(imageLink):
    ri = RevImg()
    best_guess = ri.get_best_guess("https://gimmedelicious.com/wp-content/uploads/2014/03/Cauliflower-Crust-Pizza-1-500x500.jpg")
    return best_guess

def removeNouns(best_guess):
    lines = 'lines is some string of words'
    # function to test if something is a noun
    is_noun = lambda pos: pos[:2] == 'NN'
    # do the nlp stuff
    tokenized = nltk.word_tokenize(best_guess)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
    return (' '.join(nouns)) 
    
def get_recipe(recipe_url):
    
    scraper = scrape_me(recipe_url)
    print(type(scraper.title()))
    print(type(scraper.instructions()))
    
    myIngredients = scraper.ingredients()
    myIngredientsString = ', '.join(myIngredients[1:])
    print(myIngredientsString)
    # creating a image object  
    image = Image.open(r'test.jpg')  
    
    draw = ImageDraw.Draw(image)  
    
    # specified font size 
    
    image = Image.open(r'test.jpg') 
    fontsize = 20  # starting font size
    font = ImageFont.truetype('gillsans.ttf', fontsize) 
    text1 = myIngredientsString

    text_color = (0, 0, 0)
    text_start_height = 5
    draw_multiple_line_text(image, scraper.title(), font, 'red', text_start_height)
    draw_multiple_line_text(image, "Ingredients", font, 'red', 50)
    draw_multiple_line_text(image, text1, font, text_color, 75)
    draw_multiple_line_text(image, "Instructions", font, 'red', 575)
    draw_multiple_line_text(image, scraper.instructions(), font, text_color, 600)
    image.save('pil_text.png')

def draw_multiple_line_text(image, text, font, text_color, text_start_height):
   
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=40)
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((image_width - line_width) / 2, y_text), 
                  line, font=font, fill=text_color)
        y_text += line_height

def find_recipe(food):
    
    myString = "https://www.foodnetwork.com/search/" + food.replace(" ","-") + "-/CUSTOM_FACET:RECIPE_FACET"
    URL = myString
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib 
    parsedText = soup.prettify()
    startOne = parsedText.find('o-ResultCard__m-MediaBlock m-MediaBlock')
    parsedUpate = parsedText[startOne:]
    startTwo = parsedUpate.find('www')
    parsedUpdate2 = parsedUpate[startTwo:]
    end = parsedUpdate2.find('"')
    return ("https://" + parsedUpdate2[:end])

def main():

    listener = StdOutListener()
    stream = Stream(auth, listener)
    stream.filter(track=['@MBCOVID19BOT'])

    best_guess = bestImageGuess("nope")
    food = removeNouns(best_guess)
    recipe_url = find_recipe(food)
    get_recipe(recipe_url)

if __name__ == "__main__":
    main()