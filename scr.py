from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time


url = 'https://www.trustpilot.com/categories/airlines_air_travel'

driver = webdriver.Chrome('/home/spctr/install/chromedriver_linux/chromedriver')
driver.get(url)


#return the list of company review pages
def comp_url():
    a_list = driver.find_elements_by_xpath('//a[@class="internal___1jK0Z wrapper___26yB4"]')
    urls = [a.get_attribute('href') for a in a_list]
    return urls 

# if next page button exists
def nxt_page():
    try:
        nxt_btn = driver.find_element_by_xpath('//a[@class="paginationLinkNormalize___scOgG paginationLinkNext___1LQ14"]')
        nxt_pg_link = nxt_btn.get_attribute('href')
        return True, nxt_pg_link
    except NoSuchElementException:
        return False, None


def run():
    flag = True
    url_list = []
    while flag:
        time.sleep(2)   # wait to load the elements
        url_list.extend(comp_url())
        flag, nxt_url = nxt_page()
        if flag:
            driver.get(nxt_url)

    return url_list

# it will get all urls with xpath (class) there are some other elements also which are not review links
# so remove them from list in final_url
all_urls = run()
final_url = [x for x in all_urls if x.startswith('https://www.trustpilot.com/review/')]

#writing all the urls to csv file
df = pd.DataFrame(final_url, columns= ['url'] )
df.to_csv('data.csv', index= False)


driver.close()