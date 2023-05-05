from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import time
import json
from tqdm import tqdm

class FBbot:
    def __init__(self,link):
        self.driver = uc.Chrome()
        self.driver.get(link)
        time.sleep(1)
        with open('loginData.json','r') as f:
            loginData = json.load(f)
        email = self.driver.find_element_by_id('email')
        email.send_keys(loginData['email'])
        passwrd = self.driver.find_element_by_id('pass')
        passwrd.send_keys(loginData['pass'])
        loginBtn = self.driver.find_element_by_id('loginbutton')
        loginBtn.submit()
        with open('CommentList.txt','r') as f:
            raw_cmnts = f.read().strip().split('\n')
            while '' in raw_cmnts or ' ' in raw_cmnts:
                if '' in raw_cmnts:
                    raw_cmnts.remove('')
                else:
                    raw_cmnts.remove(' ')
            with open('Comments.json', 'w+') as f:
                f.write('{\n"comments" : [\n')
                for comment in raw_cmnts:
                    f.write('"'+comment+'",\n')
                    f.write(']\n}')

    def autoComment(self,comments):
        for comment in tqdm(comments, total=len(comments)):
            commentBtn = self.driver.find_element_by_xpath('//a[@data-testid="UFI2CommentLink"]')
            commentBtn.click()
            time.sleep(2)
            commentBox = self.driver.switch_to.active_element
            commentBox.send_keys(comment)
            commentBox.send_keys(Keys.ENTER)
            time.sleep(1)
            self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)    # Scrolling to the top of the page.......
            time.sleep(1)

if __name__ == '__main__':
    bot = FBbot('***The Facebook Post ID link goes here***')
    with open('comments.json','r') as f:
        cmnts = json.load(f)['comments']
    confir = input('Please block the pop-up (type anything and press enter after dojng that) : ')
    bot.autoComment(cmnts)
    bot.driver.close()