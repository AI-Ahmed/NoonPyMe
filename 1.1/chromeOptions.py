from selenium.webdriver.chrome.options import Options


def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    
        1. Explicitly saying that this is a headless application with --headless
        2. Explicitly bypassing the security level in Docker with --no-sandbox . Apparently as Docker deamon always runs as a root user, Chrome crushes.
        3. Explicitly disabling the usage of /dev/shm/ . The /dev/shm partition is too small in certain VM environments, causing Chrome to fail or crash.
        4. Disabling the images with chrome_prefs["profile.default_content_settings"] = {"images": 2} .
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options