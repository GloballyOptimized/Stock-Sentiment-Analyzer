import pywhatkit
from textblob import TextBlob
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
#........................................................................................................................
#List of variables 
user_whatsapp_number = '' #Enter number on which you wanna have updates 
user_portfolio_stocks = [] #enter all stocks you wanna analyze 
moneycontrole_landing_page_url = 'https://www.moneycontrol.com/news/india/'#enter the media site you wanna scan 
webdriver_path = ''

#........................................................................................................................
#Extract all urls from main news page...
def get_url_list(webdriver_path,landing_page_url,url_list=[])->list:
    driver = webdriver.Chrome(webdriver_path)
    driver.maximize_window()
    driver.get(landing_page_url)
    links = driver.find_elements(By.TAG_NAME,'a')

    for link in links:
        url = link.get_attribute('href')
        url_list.append(url)

    return url_list

#........................................................................................................................
#Get text form news url
def url_to_text(url_list,webdriver_path,final_news_text_list=[])->list:
    for url in url_list:
        driver = webdriver.Chrome(webdriver_path)
        driver.maximize_window()
        driver.get(url)
        driver.implicitly_wait(15)
        all_data = driver.find_elements(By.TAG_NAME,'p')
        driver.implicitly_wait(15)
        article_data_container = []
        for data in all_data:
            article_data_container.append(data.get_attribute('innerText'))
        final_news_text_list.append(article_data_container)

        driver.quit()
    
    return final_news_text_list

#........................................................................................................................
#text leveller and cleaner 
def text_cleaner(article_text_list,final_list=[])->list:
    for article in article_text_list:
        final_list.append(','.join(article)) #to remove all the commas and convert an artile to a single string 

    return final_list
#........................................................................................................................
# find the keyword in the article 
def is_stock_in_news(user_stock_list,news_article_list,effective_article_list=[]):
    for stock in user_stock_list:
        start = 0 
        end = len(stock)
        x = 0
        while x < len(news_article_list):
            article = news_article_list[x]
            i = end
            while i < len(article):
                if article[start,end] == stock:
                    effective_article_list.append(x)
                    break
                start+=1
                end+=1
                i+=1

            x+=1
    return effective_article_list

#........................................................................................................................
#News Sentiment Aanlysis
def get_polarity(text):
    testimonial = TextBlob(text)
    return testimonial.sentiment.polarity

def get_subjectivity(text):
    testimonial = TextBlob(text)
    return testimonial.sentiment.subjectivity

#........................................................................................................................
#Send message to the user about the current stock activity 
def send_whatsapp_messages(polarity,subjectivity,phone_number,article_url):
    if polarity > 0 and subjectivity < 0.8:
        positive_message = f"Your listed word was found in this article URL ({article_url}) with market positive sentiment"
        pywhatkit.sendwhatmsg_instantly(phone_number,positive_message)
        return
    elif polarity < 0 and subjectivity < 0.8:
        negative_message = f"Your listed word was found in this article URL ({article_url}) with market negative sentiment"
        pywhatkit.sendwhatmsg_instantly(phone_number,negative_message)
        return 
    return
#........................................................................................................................
#Push update about multiple article 
def push_updates(all_articles_text_list,active_article_index):
    all_article_url = get_url_list(webdriver_path,moneycontrole_landing_page_url)
    for article in active_article_index:
        polarity = get_polarity(all_articles_text_list[article])
        subjectivity = get_subjectivity(all_articles_text_list[article])
        article_url = all_article_url[article]
        send_whatsapp_messages(polarity,subjectivity,user_whatsapp_number,article_url)
        sleep(40)
    return
#........................................................................................................................
