from datetime import datetime
import time
import csv
from driver import webDiv

from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException
from urllib3.exceptions import MaxRetryError
from custom_logger import set_logger
# from icecream import ic

LOGGER = set_logger('scraping_building_file')

# def execute_time ():
#     return f"{datetime.now()} | "

# ic.configureOutput(prefix=execute_time)


class NPM(webDiv):
        
    @staticmethod
    def fileDate():
        return datetime.now().strftime("%d-%m-%Y | %H:%M:%S")

    @classmethod
    def products_found(cls, driver, delay: int) -> int:
        """Product found is a function that scrapes the total number of products in the result page, so it can scrape on each product in the container and get the url of each product

        Args:
            webdriver (WebDriver): {"Chrome Browser": 'ChromeDriver', "FireFox Browser": 'gekodriver'}
                A browser driver for helping to build an remoted browser to start interacting with the website's: HTML, CSS, and JavaScript. 
                    
            delay (int): Maximum timeout per seconds to wait the element to be appeared in the result page.

        Returns:
            int : No. of products found in the page.
        """
        return int(wait(driver, delay).until(EC.presence_of_element_located((By.XPATH,"//div[@class='sc-14cxujr-2 izmBnU']/h2"))).text.rsplit(' ',1)[0].rsplit(' ',1)[0])


    def __init__(self, browser: str, driverPATH:str, scraping_link: str) -> None:
        """noonPyMe is a module that's scraping the products & seller infomation from noon.com website. 
        By inserting the link of your category to this module, it will automatically scrape the data of products and insert it into .csv file.

        Args:
                Type of browser which user using to start build the browser profile.
                
            browser (str): {"Chrome Browser": 'chrome', "FireFox Browser": 'firefox'}
            
            driverPATH (WebDriver): {"Chrome Browser": 'ChromeDriver', "FireFox Browser": 'gekodriver'}
                A browser driver for helping to build an remoted browser to start interacting with the website's: HTML, CSS, and JavaScript.
                
            scraping_link (str): A link of one of noon categories' pages that you want to scrape.
        """
        # ic("Building the structure...")
        LOGGER.debug('Building the structure...')
        super().__init__(browser=browser, driverPATH=driverPATH, scraping_link=scraping_link)
        self.__driver__ , self._open_driver__ =  super(NPM, self).driverProfile()
        self.containers = []
        
        self.number_of_products = None 

    
    def search(self, keyword: str, delay: int, filename: str) -> None:
        """search method allows the user to be able to enter the keyword that he/she is looking for and the problem start searching
        into noon.com for the products that user is looking for.

        Args:
            keyword (str): string letters which user enters to start searching about products to scrape in noon.com
            delay (int): A link of one of noon categories' pages that you want to scrape.
            filename (str): output CSV name that user collects his/her data into.
        """
        try:
            # first we're going to open noon.com
            self._open_driver__
            inputElement = self.__driver__.find_element_by_id('searchBar')
            inputElement.send_keys(keyword)
            inputElement.send_keys(Keys.ENTER)
            wait(self.__driver__, delay).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='productContainer']")))
        except (NoSuchElementException, TimeoutException) as err:
            self.__driver__.quit()
            LOGGER.warning("Keyword you're looking for is not found in noon.com")

        else:
            LOGGER.info(f'Keyword "{keyword}" -> Found!')
            self.deploy(delay, filename)
            
    def deploy(self, delay: int, filename:str) -> None:
        """This method is scraping all the links of the products from the containers in the page results and store in into a list.

        Args:
            delay (int): Maximum timeout per seconds to wait the element to be appeared in the result page.
            filename (str): output CSV name that user collects his/her data into.
        """
        # first we're going to open noon.com
        self._open_driver__
        try:
            self.number_of_products = NPM.products_found(self.__driver__, 5)
        except TimeoutException:
            time.sleep(3)
            self.number_of_products = NPM.products_found(self.__driver__, 5)
        
        # ic(f"Total Number of products | {self.number_of_products}")
        LOGGER.info(f"Total Number of products | {self.number_of_products}")
        try:
            while len( self.containers) != self.number_of_products:
                self.containers.extend(container.get_attribute('href') for container in wait(self.__driver__, delay).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='productContainer']/a[@href]"))))
                LOGGER.info(f"Total Number of linked scraped | {len( self.containers)} product(s)")
                try:
                    if wait(self.__driver__, delay).until(EC.presence_of_element_located((By.XPATH,"//li[@class='next']/a[@aria-disabled]"))).get_attribute('aria-disabled') == "false":
                        try:
                            self.__driver__.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            nextPage = wait(self.__driver__, delay).until(EC.presence_of_element_located((By.XPATH,"//li[@class='next']/a")) )
                            self.__driver__.execute_script("arguments[0].click()", nextPage)
                            time.sleep(3)
                        except NoSuchElementException as err:
                            pass
                except TimeoutException as err:
                    self.scraping_products_info(filename)
        except  MaxRetryError as err:
            self.__driver__.quit()
                
        except NoSuchWindowException as err:
            LOGGER.error(err)

    def scraping_products_info(self, fileName: str) -> None:
        """This method iterate over the products links; accessing it; and scraping all the information of each products.
        No need to add date or any type of formating at the end of the name, everything will be decorated and prepare for output

        Args:
            fileName (srt): This is the file name that user will add for output file.
        """
        file = fileName+' ' +NPM.fileDate()+'.csv'
        log = '/output/' + file  # Docker build
        headers = "sellerSku,EAN,Brand,Name,Description_text,Description_tags,images,price,discount,discount_value,discount_amount,currency,product_rating,product_raters,sellerName,seller_rating,seller_raters \n"
        try:
            with open(log, 'w') as writeFile:
                writeFile.write(headers)
                
                # Link all over all products and scrape data.
                for index, product in enumerate(self.containers):
                    # access the product page link
                    self.__driver__.get(product)
                    
                    # Product Essential data
                    try:
                        product_sku = self.__driver__.find_element_by_xpath("//div[@class='modelNumber']").text.rsplit(' ', 1)[-1]
                    except NoSuchElementException:
                        product_sku = 0
                    
                    try:
                        product_brand = self.__driver__.find_element_by_xpath("//div[@class='sc-1vbk2g0-7 MCFyV']").text
                    except NoSuchElementException:
                         product_brand = ' '
                    
                    product_name = self.__driver__.find_element_by_xpath("//h1[@class='sc-1vbk2g0-8 cfCaBu']").text.replace(', ', ' | ')
                    
                    try:
                        product_desc_text = self.__driver__.find_element_by_xpath("//div[@class='xf6b4m-4 fAnzcw']").text
                        product_desc_tag = self.__driver__.find_element_by_xpath("//div[@class='xf6b4m-4 fAnzcw']").get_attribute('innerHTML')

                    except NoSuchElementException:
                            product_desc_text = product_name
                            product_desc_tag = product_name
                            
                    try:
                        protduct_image = self.__driver__.find_element_by_xpath("//div[@class='sc-1xjgu8-2 lgLLLe']/img").get_attribute('src')
                        product_EAN = protduct_image.rsplit('/', 1)[-1].rsplit('_',1)[0]
                    except NoSuchElementException:
                            protduct_image = ' '
                            product_EAN = ' '
                    try:
                        product_mainPrice = self.__driver__.find_element_by_xpath("//div[@class='priceWas']").text
                        product_priceAmount = product_mainPrice.rsplit(' ',1)[-1]
                        product_currency = product_mainPrice.rsplit(' ',1)[0]
                        
                        product_discountPrice = self.__driver__.find_element_by_xpath("//div[@class='priceNow']").text.rsplit(' ', 1)[0].rsplit('\n', 1)[0].rsplit(' ',1)[0].rsplit(' ',1)[1]
                        product_discount_percentage = self.__driver__.find_element_by_xpath("//div[@class='priceSaving']/span").text.rsplit(' ', 1)[0]
                        product_discount_amount = self.__driver__.find_element_by_xpath("//div[@class='priceSaving']").text.rsplit(' ',1)[0].rsplit('\n', 1)[0].rsplit(' ',2)[1]

                    except  NoSuchElementException:
                        try:
                            product_mainPrice = self.__driver__.find_element_by_xpath("//div[@class='priceNow']").text
                            product_priceAmount = product_mainPrice.rsplit(' ', 1)[0].rsplit('\n', 1)[0].rsplit(' ',1)[0].rsplit(' ',1)[1]
                            product_currency = product_mainPrice.rsplit(' ', 1)[0].rsplit('\n', 1)[0].rsplit(' ',1)[0].rsplit(' ',1)[0]
                            
                            product_discountPrice = 0
                            product_discount_amount = 0
                            product_discount_percentage = 0
                        
                        except NoSuchElementException:
                            product_mainPrice = 0
                            product_priceAmount = 0
                            product_currency = 0
                                                    
                    ## -----------------------------------------------------------------------------------------------------------------------------------------
                    # Analytics data
                    ## Product rating
                    try:
                        product_rating = self.__driver__.find_element_by_xpath("//div[@class='scoreTag']").text
                        product_no_of_raters = self.__driver__.find_element_by_xpath("//div[@class='sc-1gzgd1-0 jLOGcR']/span").text.rsplit(' ',1)[0]
                        
                        if 'K' in product_no_of_raters:
                            product_no_of_raters = product_no_of_raters.lstrip('.').replace('K', '00')

                    except NoSuchElementException:
                        product_rating = 0
                        product_no_of_raters = 0
                        
                    ## Seller rating
                    try:
                        seller_name = self.__driver__.find_element_by_xpath("//div[@class='sc-1rmwk34-2 lhHnba']/div/div/span//a[@class='storeLink']").text
                        seller_rating = self.__driver__.find_element_by_xpath("//div[@class='starWrapper']//div[@class='starRating']").text.rsplit('(',1)[1].rsplit(')',1)[0]
                        seller_no_of_raters = self.__driver__.find_element_by_xpath("//div[@class='detail_percentage']").text
                        
                        if 'K' in seller_no_of_raters:
                            seller_no_of_raters = seller_no_of_raters.replace('.', '').replace('K', '00')
                            
                    except NoSuchElementException:
                        try:
                            seller_name = self.__driver__.find_element_by_xpath("//a[@class='storeLink']").text
                        except NoSuchElementException:
                            seller_name = ' '
                            
                        seller_rating = 0
                        seller_no_of_raters = 0
                    
                    rows = csv.writer(writeFile, dialect='excel')
                    rows.writerow([str(product_sku), str(product_EAN), str(product_brand), str(product_name), str(product_desc_text), str(product_desc_tag), \
                            str(protduct_image), str(product_priceAmount),str(product_discountPrice),str(product_discount_percentage),str(product_discount_amount),\
                            str(product_currency), str(product_rating),str(product_no_of_raters),str(seller_name),str(seller_rating),str(seller_no_of_raters)])
       
                    LOGGER.info(f"Product No. {index} | Scraped!")
                 
        except NoSuchWindowException as err:
            LOGGER.error(err)
            # ic(err)
            pass
        finally:
            try:
                writeFile.close()
                self.__driver__.close()
                LOGGER.info(f"File Downloading.....")
                time.sleep(5)
                LOGGER.info(f"Scraping Done!")
            except UnboundLocalError as err:
                LOGGER.info(err)
                pass
