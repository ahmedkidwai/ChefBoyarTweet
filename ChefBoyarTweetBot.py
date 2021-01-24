import nltk
import requests
from recipe_scrapers import scrape_me
from RevImg import RevImg
from textblob import TextBlob
from bs4 import BeautifulSoup

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
    
def get_recipe(food):
    
    scraper = scrape_me('https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/')

def find_recipe(food):
    
    myString = "https://www.foodnetwork.com/search/" + food.replace(" ","-") + "-/CUSTOM_FACET:RECIPE_FACET"
    URL = myString
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib 
    parsedText = soup.prettify()
    startOne = parsedText.find('o-ResultCard__m-MediaBlock m-MediaBlock')
    parsedUpate = parsedText[startOne:]
    #print(parsedUpate)
    startTwo = parsedUpate.find('www')
    parsedUpdate2 = parsedUpate[startTwo:]
    end = parsedUpdate2.find('"')
    print(parsedUpdate2[:end])

def main():
    best_guess = bestImageGuess("nope")
    food = removeNouns(best_guess)
    recipe_url = find_recipe(food)
    # get_recipe(food)

if __name__ == "__main__":
    main()