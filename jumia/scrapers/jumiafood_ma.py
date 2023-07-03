import json
import var.constants as const
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

class JumiaFoodMa(uc.Chrome):

    def __init__(self, teardown=False):

        self.teardown = teardown
        options = uc.ChromeOptions()
        options.add_argument("--headless")
        super(JumiaFoodMa, self).__init__(options=options)
        self.implicitly_wait(15)

    def __exit__(self, exc_type, exc_val, exc_tb):

        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.JUMIA_MA)

    def first_popup(self):
        try:
            popup = self.find_element(
                by=By.XPATH, 
                value='//header//i[@class="delete"]'
                )
            popup.click()
        except:
            pass

    def get_tags(self, index):
        try:
            return True if self.css(f'//*[@id="restaurant-list"]/section[2]/div[2]/div/article[{index+1}]/a/div[2]/span').text.strip() else False
        except:
            return False
        
    def get_restaurants_url(self):
        data = []
        for i, restaurant in enumerate(self.find_elements(By.XPATH, value='//*[@id="restaurant-list"]//article/a')):
            data.append({'restaurantUrl':[restaurant.get_attribute('href')],
                         'closedTag': [self.get_tags(i)],
                         'country': ['Morocco'],
                         'currency': ['Dh'],
                         })
        return data
    
    def close_popup(self):
        try:
            popup = self.find_element(
                by=By.XPATH, 
                value='//*[@id="jf"]/main/main/div[2]/div/header/div/button'
                )
            popup.click()
        except:
            pass

    def get_restaurant(self, row, data):

        self.get(row['restaurantUrl'][0])
        details = json.loads(self.find_element(By.XPATH, value='//*[@id="jf"]/main/script[1]').get_attribute('innerHTML').strip())
        item = {'name' : [details['name']],
        'PaymentAccepted' : [details['paymentAccepted']],
        'category' : [details['servesCuisine']],
        'address' : [details['address']['streetAddress']],
        'city' : [details['address']['addressLocality']],
        'region' : [details['address']['addressRegion']],
        'rating' : [details['aggregateRating']['ratingValue']],
        'totalRatings' : [details['aggregateRating']['reviewCount']],    
        'longitude' : [details['geo']['longitude']],
        'latitude' : [details['geo']['latitude']],
        'deliveryPrice' : [details['potentialAction']['priceSpecification']['price']]}

        try:
            tags = self.find_elements(By.XPATH, value='//*[@id="jf"]//p[@class="mbs"]/b')
            discounts_content = [content.text.strip() for content in self.find_elements(By.XPATH, value='//*[@id="jf"]/main/main/div/div/section/section[2]/div[2]/div/div/p')]
            item['discount'] = [[{'tag':tag.text.strip(),
                            'description': description}
                        for tag, description in list(zip(tags, discounts_content))]]
        except:
            item['discount'] = [[{'tag': '',
                                'description': ''}]]
        item = {**row, **item}
        return item