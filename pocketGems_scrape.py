from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_soup(url):
    """
    The webpage scrapper for list of all dogs. Design for rocketdogrescue.com
    param:
        url: the link to webpage holding dog's infor, can be the archive or to
            _be adopted info.
    return:
        soup: the object that holds all information.
    """
    try:
        response = requests.get(url, headers={'User-Agent': "PuppyLover"})
    except ValueError as e:
        print(str(e))
        return
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return soup

def scrape_summary(soup):
    """
    This function is to scrape the stuffs' summary info
    Designed for Pocket Gems
    input:
        soup: beautifulsoup of the webpage
    return:
        df: DataFrame of the stuffs' summary info
    """
    names = []
    titles = []
    backgrounds = []
    fav_games = []
    game_chars = []
    
    for stuff in soup.find_all("figure", {"class": "item"}):
        try:
            name = stuff.strong.text
            background = stuff.find_all("p")[1].text
            fav_game = stuff.find_all("p")[3].text
            game_char = stuff.find_all("p")[5].text

            name_title = stuff.figcaption.text.split()        
            for n in name.split():
                name_title.remove(n)
            title = " ".join(name_title)

            names.append(name)
            titles.append(title)
            backgrounds.append(background)
            fav_games.append(fav_game)
            game_chars.append(game_char)
        # Print the HTML info if there is something wrong
        except:
            print(stuff)
    
    df = pd.DataFrame({'name': names, 'title': titles, 'background': backgrounds, 
                      'fav_game': fav_games, 'game_char': game_chars})
    
    return df   

if __name__ == "__main__":
    url = 'https://pocketgems.com/about/'
    soup = get_soup(url)
    df = scrape_summary(soup)
    df.to_csv('pocket_gems.csv', index=False)
