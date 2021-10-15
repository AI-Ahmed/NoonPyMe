from noonPyMe import NPM
from header import program_header
from custom_logger import set_logger

LOGGER = set_logger('deploying_the_interface')

if __name__ == '__main__':
    program_header('1.0')
    try:
        # browser = str(input('Enter the your browser name (chrome, or firefox): ')) #offline
        # browser = 'firefox' #offline
        browser = "chrome"
        driver = ' '
        scrapingUrl = str(input('Enter the noon link page: '))
       
        filename = str(input("Enter your file name: "))
        delay = int(input("Enter the delay time [seconds >= 3]: "))

        LOGGER.info('Building and Debugging info...')
       
        scrape = NPM(browser,driver, scrapingUrl)
        scrape.deploy(delay, filename)
    except (TypeError, ValueError) as err:
        print(f'Deploy Error | {err}')