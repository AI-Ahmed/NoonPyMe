from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from custom_logger import set_logger

from typing import Tuple
from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver import FirefoxOptions

LOGGER = set_logger('driver_connection')

class webDiv:
    
    def __init__(self, driverName: str, driverPATH:str, scraping_link: str) -> None:
        """This is the parent class which responsible for everything related to the connection with webdrivers and any type of drivers that the program support –
        also, it's responsible for all the requests comming from other modules that want to build web driver for itself to execute scraping or automation process.

        Args:
             driverName (str): {"Chrome Browser": 'chrome', "FireFox Browser": 'firefox'}
                Type of browser which user using to start build the browser profile.
            
            driverPATH (WebDriver): {"Chrome Browser": 'ChromeDriver', "FireFox Browser": 'gekodriver'}
                A browser driver for helping to build an remoted browser to start interacting with the website's: HTML, CSS, and JavaScript.
                
            scraping_link (str): A link of one of noon categories' pages that you want to scrape.
        """
        self._driver_name_ = driverName
        self.__driver__PATH__ = driverPATH
        self._url = scraping_link
        LOGGER.info('Driver debugging...')
    
    def set_chrome_options(self) -> Options:
        """Sets chrome options for Selenium.
        Chrome options for headless browser is enabled.
        
            1. Explicitly saying that this is a headless application with --headless
            2. Explicitly bypassing the security level in Docker with --no-sandbox . Apparently as Docker deamon always runs as a root user, Chrome crushes.
            3. Explicitly disabling the usage of /dev/shm/ . The /dev/shm partition is too small in certain VM environments, causing Chrome to fail or crash.
            4. Disabling the images with chrome_prefs["profile.default_content_settings"] = {"images": 2} .
        Returns:
            Options (Options): chrome parameters for handling the driver
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        return chrome_options
    
    def set_firfox_options(self)-> Tuple[FirefoxProfile, FirefoxOptions]:
        fp = FirefoxProfile()
        fp.set_preference("http.response.timeout", 5)
        fp.set_preference("dom.max_script_run_time", 5)

        options = FirefoxOptions()
        options.add_argument('-headless')
        
        return fp, options
    
    def driverProfile(self):
        """Selenium is one of the interactive libraries that helps you to interact and test the performance of websites. Besides, it helps you to scrape the data you want even if the data debugged by javaScript
        Here, we're building Firefox driver to help us to access noon.com website for scraping it.
        
        Args:
            driverName (str): {"Chrome Browser": 'chrome', "FireFox Browser": 'firefox'}
                Type of browser which user using to start build the browser profile.
            
            driverPATH (WebDriver): {"Chrome Browser": 'ChromeDriver', "FireFox Browser": 'gekodriver'}
                A browser driver for helping to build an remoted browser to start interacting with the website's: HTML, CSS, and JavaScript.
                
            url (str): This is the link that you provide to the driver to access the website, remotely.
            
        Returns:
            WebDriver.windows.interaction : Execute the url given to open the windows of the driver to start interacting
        """
        chrome_options = self.set_chrome_options()
        if self._driver_name_ == "chrome":
            try:
                driver = webdriver.Chrome(options=chrome_options)
                driver.set_window_size(800, 600)
                
                return driver, driver.get(self._url)
            except (WebDriverException, UnboundLocalError) as err:
                LOGGER.error(err)
                # ic(err)
                pass
                
        elif self._driver_name_ == "firefox":
            ffp, ffo = self.set_firfox_options()
            try:
                driver = webdriver.Firefox(executable_path=self.__driver__PATH__, firefox_profile=ffp, options=ffo)
                driver.set_window_size(1200, 800)
                
                return driver, driver.get( self._url)
            
            except (WebDriverException, UnboundLocalError) as err:
                LOGGER.error(err)
                # ic(err)
