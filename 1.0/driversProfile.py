import selenium.webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.common.exceptions import WebDriverException
from chromeOptions import set_chrome_options
from custom_logger import set_logger
from firefoxOptions import set_firfox_options
# from icecream import ic

LOGGER = set_logger('reading_profile')

def driverProfile(driverName, driverPATH, url):
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
    webdriver = selenium.webdriver
    chrome_options = set_chrome_options()
    if driverName == "chrome":
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_window_size(800, 600)
            
            return    driver, driver.get(url)
        except (WebDriverException, UnboundLocalError) as err:
            LOGGER.error(err)
            # ic(err)
            
    elif driverName == "firefox":
        ffp, ffo = set_firfox_options()
        try:
            driver = webdriver.Firefox(executable_path=driverPATH, firefox_profile=ffp, options=ffo)
            driver.set_window_size(1200, 800)
            
            return    driver, driver.get(url)
        except (WebDriverException, UnboundLocalError) as err:
            print('cocococ')
            LOGGER.error(err)
            # ic(err)
    
