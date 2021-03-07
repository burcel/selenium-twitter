from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
import os
import time


class Driver:
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
    URL = "https://twitter.com/search?q={}%20lang%3Aen&src=typed_query&f=live"

    def __init__(self):
        self.driver = None
        self.script_path = os.path.dirname(os.path.abspath(__file__))
        self.chrome_driver_path = os.path.join(self.script_path, "chromedriver.exe")
        self.url = self.URL.format("bitcoin")

    def init_driver(self) -> None:
        """
        Initialize web driver
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("user-agent={}".format(self.USER_AGENT))
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # Disable images

        self.driver = webdriver.Chrome(self.chrome_driver_path, chrome_options=chrome_options)

    def close_driver(self) -> None:
        """
        Close web driver
        """
        if self.driver is not None:
            self.driver.close()

    def return_scroll_height(self) -> int:
        """
        Return scroll height as int
        """
        return self.driver.execute_script("return document.body.scrollHeight")

    def parse_tweet(self, web_element: WebElement) -> None:
        """
        Parse tweet from web element and return
        :return:
        """
        # TODO
        pass

    def fetch_tweets(self) -> None:
        """
        Start the process of fetching tweets
        """
        self.init_driver()
        self.driver.get(self.url)
        # driver.set_window_size(1024, 768)

        tweet_section = self.driver.find_element_by_xpath('//section[@aria-labelledby="accessible-list-0"]/div/div')
        tweet_index = 0
        last_height = self.return_scroll_height()
        while True:
            # TODO
            tweet_divs_list = tweet_section.find_elements_by_xpath("./div")

            for tweet_div in tweet_divs_list:
                self.parse_tweet(tweet_div)

            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(1)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.return_scroll_height()
            if new_height == last_height:
                break
            last_height = new_height


if __name__ == "__main__":
    driver = Driver()
    driver.fetch_tweets()
