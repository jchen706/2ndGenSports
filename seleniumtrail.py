## Using selenium to help scrap javascript websites
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from time import sleep
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import lxml
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import TweetTokenizer, sent_tokenize
from nltk.tokenize import word_tokenize
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


#update the Chrome version 81
webdriver_url = "./chromedriver.exe"

#For windows you have to use path
# phantomjs_url="C:/Users/jchen/Documents/2ndGenSports/phantomjs-2.1.1-windows/bin/phantomjs.exe"
# driver = webdriver.PhantomJS(phantomjs_url)
def initalize_driver():
    return 0




#For Mac / Linuc
#driver=webdriver.PhantomJS()
#driver = webdriver.Chrome(webdriver_url)
def selenium_option(roster_url, sport, base_url):
    print(sport)
 
    print('into selenium')
    chrome_options = None
    try:
        chrome_options = webdriver.ChromeOptions() 
    except Exception as err:
        print(err.message())
    chrome_options.headless=True
    print("options not working")
    chrome_options.add_argument("--headless")
    print("options not working")
    chrome_options.add_argument("--no-sandbox")
    print("options not working")

    chrome_options.add_argument("--disable-gpu")
    print("options not working")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36")
    print('initalize webdriver')
    driver = webdriver.Chrome(options=chrome_options, executable_path=webdriver_url)
   
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
    """
    })
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browser1"}})

   


 
    print('before get')
    driver.get(roster_url)
    element=None
    print('before try')
    try:
        element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.TAG_NAME, "td"))
        )
   
        
    finally:
        #print(driver.page_source)
        new_soup = BeautifulSoup(driver.page_source, 'lxml')
        #print(new_soup)
        a1 = new_soup.find_all("a", href=True)
        team_links, not_normal_name = parse_links(a1, sport)
        driver.quit()
        
        print(len(team_links))

        return_dict = run_all(team_links, chrome_options, base_url)

        return return_dict
       
      
                
      


def run_all(team_links, chrome_options, base_url):
    team_dict = {}
        
    wantedList=['parent','Parents', 'Father', 'Mother', 'father', 'mother', 'dad', 'Dad', 'Mom', 'mom', 'son', 'Son', 'daughter', 'Daughter']


    for key, value in team_links.items():
        driver = webdriver.Chrome(options=chrome_options, executable_path=webdriver_url)
       
        
        true_list = []
        player_name = key
        print(player_name)
       
        if value[:5] == 'https':
            newURL = value
        else:
            newURL = base_url + value

        print(newURL)
        
        driver.get(newURL)
        element=None
        print('before try')
        try:
            #class="story-content roster-h3 ng-binding"
            #element = WebDriverWait(driver, 30)
            #time.sleep(15)
            element = WebDriverWait(driver, 60)
            Thread.sleep(3000)
            #.until(EC.text_to_be_present_in_element((By.XPATH, "#//div[@id= 'playerbio-profile']/div/ul/li"), "the"))
            element1 = driver.find_element_by_id("playerbio-profile")
            
            if element is None:
                print("no element")
                #//div[@id= 'playerbio-profile']/div/ul
                #//div[@id= 'playerbio-profile']/div[@class='story-content roster-h3 ng-binding']/*
        except TimeoutException as error1:
                    print("Timed out waiting for page to load") 
                    pass
        except NoSuchElementException as error2:
                    print('No such element')
                    pass
        except Exception as err:
                    print('ok exception')
                    pass
        except:
            print('unexpected behavior')
            pass
                    
        
        #print(driver.page_source)
        new_soup = BeautifulSoup(driver.page_source, 'lxml')
        #print(new_soup)
        all_textlist=new_soup.body.find_all(text=True)
        print('here and there')
        with open('soup3.csv', mode='w', encoding='utf-8', newline='') as employee_file:
                                employee_writer = csv.writer(employee_file)
                                employee_writer.writerow([driver.page_source])

                   

        print('before for loop')

        for i in range(len(all_textlist)):
            for each in wantedList:
                if each in all_textlist[i].strip():
                    if 'null' not in all_textlist[i]:
                        if 'html' not in all_textlist[i]:
                            if 'https' not in all_textlist[i]:
                                if 'script' not in all_textlist[i]:
                                    if "/div" not in all_textlist[i]:
                            
                                    
                                        print('made it')
                                        tokens = word_tokenize(all_textlist[i])
                                        print(tokens)
                                        if each in tokens:
                                            print(tokens)
                                            item_append = ' '.join(tokens)
                                            
                                            if item_append in true_list:
                                                continue
                                            true_list.append(item_append)
        print('here before team_dict')
        team_dict[player_name] = true_list
        print(team_dict)

        driver.quit()   
    return team_dict
                                
                


                









        
        

        



  

def parse_links(result, sport):
    team_links = {}
    links=[]
    not_normal_name=False
    
    #for BYU
   
    for link in result:
        print("")
        print("href: {}".format(link.get("href")))
        a = link.get("href")
        link_split = a.split('/')
        print(link_split)
        if 'athlete' in link_split:
            print("here")
            print(str(sport))
            if str(sport) in link_split:
                #print("sport")
                if 'coaches' not in link_split:
                    if 'staff' not in link_split:
                        if 'coach' not in link_split:

                            #print(link_split)
                            print(link_split[-1])
                            if (link_split[2] == sport and link_split[-1].isnumeric()):
                                player_name = link_split[-1]
                                print('where there')
                                print(link.text)
                                team_links[player_name] = a
                                not_normal_name=True
                                links.append(a)
                            elif (link_split[2] == sport and link_split[1] == 'athlete'):
                                player_name = link_split[-1].split('-')
                               
                                for i in range(len(player_name)):
                                    print(player_name)
                                    player_name[i] = player_name[i][0].upper() + player_name[i][1:]
                                player_name = " ".join(player_name).strip()
                                team_links[player_name] = a
                                print(a)
                                links.append(a)

                            else:
                                print(a)
                                print('welcome')
                                player_name = link_split[len(link_split) - 1].replace('-', ' ')
                                if(link_split[-1] == "") or (str(link_split[-1]).isnumeric()):
                                    player_name = link_split[len(link_split) - 2].replace('-', ' ')



                                player_name = player_name.strip().split(' ')
                                if len(player_name) == 1 or player_name[0] == 'roster':
                                    continue
                                for i in range(len(player_name)):
                                    print(player_name)
                                    player_name[i] = player_name[i][0].upper() + player_name[i][1:]
                                player_name = " ".join(player_name).strip()
                                team_links[player_name] = a
                                print(a)
                                links.append(a)
    print(team_links)
    return (team_links, not_normal_name)
    

#selenium_option('https://byucougars.com/roster/m-basketball/', 'm-basketball', 'https://byucougars.com')


  