# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape():

    # initialise splinter and set executable path
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)

    # visit Mars News Site
    url= "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')

    slide_elem.find('div', class_='content_title')

    # Collect latest News Title
    news_title = slide_elem.find('div', class_='content_title').get_text()
    news_title

    # Collect News Title's paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    news_p

    # Identify featured images 
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag("button")[1]
    full_image_elem.click()

    # Use soup to parse the resulting html
    html = browser.html
    img_soup = soup(html, "html.parser")
    img_soup

    # Find the relative image url
    img_url1 = img_soup.find("img", class_= "fancybox-image").get("src")
    img_url1

    # Use the base URL to create an absolute URL
    featured_img_url = f"https://www.jpl.nasa.gov{img_url1}"
    featured_img_url

    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet 

    df = pd.read_html("https://galaxyfacts-mars.com/")[0]
    df.head()

    df.columns=["Description", "Mars", "Earth"]
    df.set_index("Description", inplace=True)
    df

    # Use Pandas to convert the data to a HTML table string
    df.to_html()

    # Scrape High-Resolution Mars’ Hemisphere Images and Titles

    # initialise splinter and set executable path
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)

    # visit URL with browser

    # Use browser to visit the URL 
    url = "https://marshemispheres.com/"
    browser.visit(url)

    # Create a list that holds the images' titles and URLs
    hemis_imgs_urls = []

    # Retrieve url's and titles for each hemisphere
    for i in range(4):
        #create empty dictionary
        hemispheres = {}
        browser.find_by_css("a.product-item h3")[i].click()
        element = browser.links.find_by_text("Sample").first
        img_url = element['href']
        title = browser.find_by_css("h2.title").text
        hemispheres["img_url"] = img_url
        hemispheres["title"] = title
        hemis_imgs_urls.append(hemispheres)
        browser.back()

    hemis_imgs_urls

    browser.quit

    data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_imaged": featured_img_url,
        "facts":  df.to_html(),
        "hemispheres": hemis_imgs_urls
    }
    return data


