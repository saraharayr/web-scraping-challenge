# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager

def scrape_info():
    # Set up Splinter
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    
    # visit the Mars News Site
    url = "https://redplanetscience.com/"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #  Collect latest News Title & Paragraph
    news_title = soup.find_all("div", class_="content_title")[0].get_text
    news_p = soup.find_all("div", class_="article_teaser_body")[0].get_text

    # Identify featured images 
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Use soup to parse the resulting html
    html = browser.html
    soup = bs(html, "html.parser")

    img_src = soup.find_all("img")[1]["src"]
    # Combine base url with image source to get images url
    featured_img_url = url + img_src

    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet 
    url = "https://galaxyfacts-mars.com/"

    # Pandas 
    table = pd.read_html(url)
    # Cleaning the table
    df = table[0]
    df2 = df.set_index(keys=0)
    df2.index.name=None
    df2.columns = [''] * len(df2.columns)
    # Dataframe to html
    html_table = df2.to_html(header=False)
    # Cleaning the table
    html_table = html_table.replace('\n', '')
    # Saving html to a file
    df2.to_html("table.html")

    # Scrape High-Resolution Mars’ Hemisphere Images and Title,
    #Visit URl
    url = "https://marshemispheres.com/"
    browser.visit(url)

    # Create a list that holds the images, titles and URLs
    hemis_img_urls = []
    # Retrieve url's and titles for each hemisphere
    for x in range (0,4):
        time.sleep(1)
        ####################################
        html = browser.html
        soup = bs(html, "html.parser")
        href = soup.find_all("h3")[x].text
        browser.links.find_by_partial_text(href).click()
        html = browser.html
        soup = bs(html, "html.parser")
        img_url = soup.find_all("img", class_="wide-image")[0]["src"]
        full_url = url + img_url
        title = soup.find_all("h2", class_="title")[0].text
        dictionaries = {"title": title, "img_url": full_url}
        hemis_img_urls.append(dictionaries)
        back = soup.find_all("h3")[1].text
        browser.links.find_by_partial_text(back).click()

    #  Store all values in dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_img_url,
        "html_table": html_table,
        "hemisphere_image_urls": hemis_img_urls
        }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

if __name__ == "__main__":

    print(scrape_info())
