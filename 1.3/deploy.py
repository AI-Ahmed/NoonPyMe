from header import program_header
from noonPyMe import NPM

from custom_logger import set_logger

LOGGER = set_logger('deploying_the_interface')

def rep(link:str) ->str:
    index = link.find('?')
    return link[:index] + '?limit=1000&' + link[index+1:] 


def promo() -> None:
    program_header('1.3')
    try:
        # browser = 'firefox' #offline
        browser = "chrome" # docker build
        driver = ''  # firefox driver

        sup = str(input('How would you like to search? by [Link(L)/Keyword(K)]: ')).upper()
        if sup == 'L':
            scrapingUrl = rep(str(input('Enter the noon link page: ')))
            
            filename = str(input("Enter your file name: "))
            delay = int(input("Enter the delay time [seconds >= 3]: "))
            
            npm = NPM(browser, driver, scrapingUrl)
            npm.deploy(delay, filename)
            
        elif sup == 'K':
            scrapingUrl = "https://www.noon.com"
            keyword = str(input('Enter the keyword: '))
            
            filename = str(input("Enter your file name: "))
            delay = int(input("Enter the delay time [seconds >= 3]: "))
            
            npm = NPM(browser, driver, scrapingUrl)
            npm.search(keyword, delay, filename)
        else:
            LOGGER.info('Invalid Input!')
        
    except (TypeError, ValueError) as err:
        LOGGER.error(f'Deploy Error | {err}')
        
if __name__ == '__main__':
    promo()