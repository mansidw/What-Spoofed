from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv
import tkinter as tk
from flask import Flask,request
  
# Initializing flask app
app = Flask(__name__)

load_dotenv()

# add the path here for the chromdriver and Google Chrome instance
CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')
GOOGLE_CHROME_BIN = os.getenv('GOOGLE_CHROME_BIN')
FORM_URL=os.getenv('GMAIL_LOGIN_URL')
class GmailCrawler:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(FORM_URL)
    
    def Login(self,email,password):
        self.driver.find_element("name",'identifier').send_keys(email)
        time.sleep(3)
        nextButton = self.driver.find_elements(By.XPATH,'//*[@id ="identifierNext"]')
        nextButton[0].click()
        time.sleep(3)
        passWordBox = self.driver.find_element(By.XPATH,
        '//*[@id ="password"]/div[1]/div / div[1]/input')
        passWordBox.send_keys(password)
    
        nextButton = self.driver.find_elements(By.XPATH,'//*[@id ="passwordNext"]')
        nextButton[0].click()
        time.sleep(10)
    
    def GetFirstMailsHeader(self):
        time.sleep(10)
        self.driver.find_element(By.XPATH,"(//tr[@class='zA zE'])[1]").click()
        # self.driver.find_element(By.XPATH,"(//tr[@class='zA yO'])[1]").click()
        time.sleep(4)
        self.driver.find_element(By.XPATH,"//button[@aria-label='Close']").click()
        time.sleep(3)
        self.driver.find_element(By.XPATH,"//div[@aria-label='More']").click()
        time.sleep(3)

        self.driver.find_element(By.XPATH,"//div[text()='Show original']").click()
        time.sleep(10)
        window_after = self.driver.window_handles[1]
        self.driver.switch_to.window(window_after)
        time.sleep(3)
        self.driver.find_element(By.XPATH,"//div[text()='Copy to clipboard']").click()
        time.sleep(3)
        root = tk.Tk()
        strtp=root.clipboard_get()
        # final=strtp.split("List-Unsubscribe:")[0]
        with open('header.txt', 'w',encoding="utf-8") as f:
            f.write(strtp)
        
@app.route("/tp",methods=['GET'])
def tpfuns():
    args = request.args
    print(args["email"])
    return args
        

@app.route('/data',methods=['GET'])
def get_time():
    args = request.args
    options = webdriver.ChromeOptions()
    options.binary_location = GOOGLE_CHROME_BIN
    options.add_argument("start-maximized")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument('log-level=3')
    options.add_argument("--window-size=1920,1080")
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['acceptSslCerts'] = True
    capabilities['acceptInsecureCerts'] = True
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options, desired_capabilities=capabilities)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    gmailCrawler = GmailCrawler(driver)
    print(args["password"])
    gmailCrawler.Login(args["email"],args["password"]+"#")
    time.sleep(3)

    gmailCrawler.GetFirstMailsHeader()


    import subprocess
    p=subprocess.call(['python', 'decodespamheaders.py', 'header.txt','-f','html','-o','report.html'],shell=True)

    time.sleep(4)
    import webbrowser
    webbrowser.open_new_tab('report.html')
  
    # Returning an api for showing in  reactjs
    return {"message":"Successs"}
  
      
# Running app
if __name__ == '__main__':
    app.run(debug=True)




