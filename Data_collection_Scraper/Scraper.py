
from selenium import webdriver
from selenium.webdriver.common. by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from typing import Any
import time
import datetime
import json
import os
import requests


class Web_link_scraper:    
    def __init__(self, url: str="https://www.boxofficemojo.com/", driverpath: str='/Applications/chromedriver'):     
        self.service = Service(driverpath)
        self.options = Options()
        self.driver = webdriver.Chrome(options=self.options, service=self.service) 
        self.driver.get(url)
        self.movie_link_list = []
        self.category_heading_list = []
        self.category_value_list = []
        time.sleep(3)

    def _click_monthly_button(self):
        domestic_container = self.driver.find_element(by=By.XPATH, value='//*[@id="a-page"]/div[2]/div[4]/div') 
        monthly_button = domestic_container.find_element(by=By.XPATH, value='//*[@id="a-page"]/div[2]/div[4]/div/a[4]') 
        monthly_button.click()
        time.sleep(3)

    def _select_year_from_scroll_down_menu(self):
        drop_down_list = self.driver.find_element(by=By.XPATH, value='//select[@id="view-navSelector"]') 
        select = Select(drop_down_list)
        select.select_by_visible_text('By year')
        time.sleep(3)

    def _create_list_of_movie_links(self, year_list):    
        self._select_year_from_scroll_down_menu()
        for year in (year_list): 
            drop_down_by_year = self.driver.find_element(by=By.XPATH, value='//select[@id="by-year-navSelector"]')
            select = Select(drop_down_by_year)
            select.select_by_visible_text(year)
            time.sleep(3)

            movie_table = self.driver.find_element(by=By.XPATH, value='//*[@id="table"]/div/table[2]/tbody')
            movie_list = movie_table.find_elements(by=By.XPATH, value='//*[@class="a-text-left mojo-field-type-release mojo-cell-wide"]')
            for movie in movie_list:
                a_tag = movie.find_element(by=By.TAG_NAME, value='a')
                link = a_tag.get_attribute('href')
                self.movie_link_list.append(link)
        # print(self.movie_link_list)
        # print(len(self.movie_link_list))
        return self.movie_link_list  


class Data_scraper(Web_link_scraper):                                                                              
    def __init__(self):
        super().__init__()
        self.image_and_text_dictionary = {}
        self.movie_dictionary = {}
        self.timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        self.file_path = os.path.join('raw_data', 'box_office_mojo')

    def __scrape_text_data_from_movie_links(self):
        summary_table = self.driver.find_element(by=By.XPATH, value='//div[@class="a-section a-spacing-none mojo-gutter mojo-summary-table"]')
        summary_values = summary_table.find_element(by=By.XPATH, value='//div[@class="a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile"]')
        div_tags = summary_values.find_elements(by=By.XPATH, value='./div[@class="a-section a-spacing-none"]')
        performance_summary_values = summary_table.find_element(by=By.XPATH, value='//div[@class="a-section a-spacing-none mojo-gutter mojo-summary-table"]')
        worldwide_values = performance_summary_values.find_element(by=By.XPATH, value='//div[3][@class="a-section a-spacing-none"]')
        worldwide_gross = worldwide_values.find_element(by=By.XPATH, value='span[1]/a').text
        self.category_heading_list.append(worldwide_gross)
        international_gross = worldwide_values.find_element(by=By.XPATH, value='span[2]/a/span').text
        self.category_value_list.append(international_gross)        

        for text in div_tags:
            category_heading = text.find_element(by=By.XPATH, value='span[1]').text
            self.category_heading_list.append(category_heading)
            category_value = text.find_element(by=By.XPATH, value='span[2]').text
            self.category_value_list.append(category_value)
              
        text_dictionary = dict(zip(self.category_heading_list, self.category_value_list))
        #print(text_dictionary)
        return text_dictionary
        
    def create_movie_dictionary(self):
        for link in (self.movie_link_list[0:3]):
            self.driver.get(link)
            time.sleep(4)
            div_tag = self.driver.find_element(by=By.XPATH, value='//div[@class="a-fixed-left-grid-col a-col-right"]')
            movie_name = div_tag.find_element(by=By.XPATH, value='h1[@class="a-size-extra-large"]').text      
            self.__create_timestamp_for_web_scrape()
            image_link = self.__scrape_image_data()
            self.image_and_text_dictionary = self.__scrape_text_data_from_movie_links()
            self.image_and_text_dictionary.update({'image_link':image_link})
            self.movie_dictionary.update({movie_name:self.image_and_text_dictionary})
        return self.movie_dictionary
            
    def __create_timestamp_for_web_scrape(self):      
        time_key = 'timestamp'
        self.category_heading_list.append(time_key)
        self.category_value_list.append(self.timestamp)

    def __scrape_image_data(self):
        image_results = self.driver.find_element(By.XPATH, value = '//*[@class="a-section a-spacing-none mojo-posters"]')
        img_tag = image_results.find_element(by=By.TAG_NAME, value='img')
        src = img_tag.get_attribute('src')
        return src   
             
    def create_directories(self):
        os.mkdir('raw_data')
        os.mkdir(self.file_path)
        
    def save_to_json(self, file_path: str, object_to_save: Any, indent: int):
        try:
            with open(os.path.join(self.file_path, 'data.json'), "w") as outfile:
                json.dump(self.movie_dictionary, outfile, indent=indent)
            return True
        
        except Exception as e:
            print(e)
            return False

    def create_image_directory(self):
        image_path = 'raw_data/box_office_mojo/images'
        os.mkdir(image_path)
        for n, movie in enumerate(self.movie_dictionary.values(),1):
                timestr = self.timestamp
                self.download_image(movie['image_link'], f'raw_data/box_office_mojo/images/{timestr}_{n}.jpg')     
    
    def download_image(self, image_url, fp):
        image_data = requests.get(image_url, fp).content
        with open(fp, 'wb') as handler:
            handler.write(image_data)
        

    
    
if __name__ == '__main__':
    year_list = ['2017', '2018']
    imdb = Data_scraper()
    imdb._click_monthly_button()
    imdb._create_list_of_movie_links(year_list)
    imdb.create_movie_dictionary()
    imdb.create_directories()
    imdb.create_image_directory()
    imdb.save_to_json(str, Any, 4)
    
