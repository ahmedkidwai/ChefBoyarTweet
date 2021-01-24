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

# # # # Global # # # #
auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,
                    twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN,
                      twitter_credentials.ACCESS_TOKEN_SECRET)
api = API(auth, wait_on_rate_limit=True,
          wait_on_rate_limit_notify=True)

class StdOutListener(StreamListener):

    def on_data(self, data):
        json_data = json.loads(data)
        # Check if original tweet is a reply (i.e we want to parse an image)
        if json_data['in_reply_to_status_id_str']:
            tweet_user = "@" + json_data['user']['screen_name']
            original_tweet_id = json_data['in_reply_to_status_id_str']
            media_url = self.get_original_tweet_image(original_tweet_id)
            imageGuess = self.best_image_guess(media_url)
            print(imageGuess)
            nounString = self.get_nouns(imageGuess)
            print(nounString)
            recipe_url = self.find_recipe(nounString)
            print(recipe_url)
            self.get_recipe(recipe_url)
            
            
        # If we want to get a recipe from a link
        else:
            print("WIP")
        # print(data)
        return(True)
    def on_error(self, status):
        print(status)
    
    def get_original_tweet_image(self, original_tweet_id):
        status = api.get_status(original_tweet_id,  tweet_mode='extended')
        json_str = json.dumps(status._json)
        start = json_str.find("media_url")
        start_url = json_str[start:]
        start2 = start_url.find("http")
        start_url2 = start_url[start2:]
        end = start_url2.find('"')
        media_url = start_url2[:end]
        return media_url


    def best_image_guess(self, media_url):
        ri = RevImg()
        best_guess = ri.get_best_guess(media_url)
        print(best_guess)
        return best_guess

    def get_nouns(self, best_guess):
        lines = 'lines is some string of words'
        # function to test if something is a noun
        is_noun = lambda pos: pos[:2] == 'NN'
        # do the nlp stuff
        tokenized = nltk.word_tokenize(best_guess)
        nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
        return (' '.join(nouns)) 
        
    def get_recipe(self, recipe_url):
        print("Yee Haw")
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
        self.draw_multiple_line_text(image, scraper.title(), font, 'red', text_start_height)
        self.draw_multiple_line_text(image, "Ingredients", font, 'red', 50)
        self.draw_multiple_line_text(image, text1, font, text_color, 75)
        self.draw_multiple_line_text(image, "Instructions", font, 'red', 575)
        self.draw_multiple_line_text(image, scraper.instructions(), font, text_color, 600)
        print("Jackpot")
        image.save('pil_text.png')

    def draw_multiple_line_text(self, image, text, font, text_color, text_start_height):
    
        draw = ImageDraw.Draw(image)
        image_width, image_height = image.size
        y_text = text_start_height
        lines = textwrap.wrap(text, width=40)
        for line in lines:
            line_width, line_height = font.getsize(line)
            draw.text(((image_width - line_width) / 2, y_text), 
                    line, font=font, fill=text_color)
            y_text += line_height

    def find_recipe(self, food):
        
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

if __name__ == "__main__":
    main()