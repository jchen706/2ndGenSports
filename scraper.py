import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import TweetTokenizer, sent_tokenize
from nltk.tokenize import word_tokenize
import urllib
#from requests_html import HTMLSession
from threading import Thread
#from requests_html import AsyncHTMLSession
import asyncio
import pyppeteer
from pyppeteer import launch
from asynccall import get_url_async
#from seleniumtrail import selenium_option

#find the items of paragraph or list in the player's page


def find_items(team_links, base_url, not_normal_name):
    team_dict = {}
    wantedList=['parent','Parents', 'Father', 'Mother', 'father', 'mother', 'dad', 'Dad', 'Mom', 'mom', 'son', 'Son', 'daughter', 'Daughter']

    for key, value in team_links.items():
        player_dic = {}
        player_array=[]
        bullet_array=[]
        player_name = key

        new_player = {}
        new_player_arr = []
        if value[:5] == 'https':
            newURL = value
        else:
            newURL = base_url + value
        print("inside find items")
        print(newURL)
        headers={}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        print('request')
       
        new_r = requests.get(newURL, headers=headers)
        
        #print(new_r.text)
        new_soup = BeautifulSoup(new_r.content, 'html.parser')
        #print("before")
        #print()
        #print("after")

        import csv

        
        all_textlist=new_soup.body.find_all(text=True)
        print(not_normal_name)
        #Illinois Illi for illinois and
        if not_normal_name:
            print('here not normal name')
            try:
                player_name_wrapper = new_soup.find('div', class_= 'player_name_wrapper')
                player_name_list = player_name_wrapper.text.strip().split('\n')
                player_name = player_name_list[-2] +" "+ player_name_list[-1]
            except Exception as e:
                pass
            #player_first_name = player_name_wrapper.find_all('div', class_= 'player_first_name')
            # print('error')
            # player_last_name = new_soup.find_all("div", class_= "player_last_name")
            # print(player_last_name)
            # print("error2")
            # print(player_first_name)
            # print('none')
        
        #print(all_textlist)

        true_list = []

        for i in range(len(all_textlist)):
            for each in wantedList:
                if each in all_textlist[i].strip():
                    if 'null' not in all_textlist[i]:
                        if 'html' not in all_textlist[i]:
                            if 'https' not in all_textlist[i]:
                                if 'script' not in all_textlist[i]:
                                    if "/div" not in all_textlist[i]:
                                    #new_list = all_textlist[i].split(' ')
                                    #
                                        tokens = word_tokenize(all_textlist[i])
                                        if each in tokens:
                                            item_append = ' '.join(tokens)
                                            
                                            if item_append in true_list:
                                                continue
                                            true_list.append(item_append)
                                       
       
        #new_soup.get_text())
        #print(new_soup.select('div'))
        ane = new_soup.select('div')
        print(true_list)

        print(len(ane))
        #periods = [pt.get_text() for pt in ane]
        # for each in periods:
        #     for wanted_word in wantedList:
        #         if wanted_word in each:
        #             #print(each)
        #             tokenizer_words = TweetTokenizer()
        #             tokens_sentences = [tokenizer_words.tokenize(t) for t in nltk.sent_tokenize(each)]
        #             print(tokens_sentences)
        #             with open('soup.csv', mode='w', encoding='utf-8', newline='') as employee_file:
        #                  employee_writer = csv.writer(employee_file)
        #                  employee_writer.writerow(tokens_sentences)
                    



        #             for i in range(len(tokens_sentences)):
        #                  for each_word in wantedList:
        #                      if tokens_sentences[i] == each_word:
        #                          new_player_arr.append(' '.join(tokens_sentences[i:]))
        #             break

                

        # with open('soup2.csv', mode='w', encoding='utf-8', newline='') as employee_file:
        #                     employee_writer = csv.writer(employee_file)
        #                     employee_writer.writerow(new_player_arr)
        

   
        




        #list_contents = new_soup.find_all("p")

        #list_contents = new_soup.find_all("li")
        #periods = [pt.get_text() for pt in period_tags]




        #for each in list_contents:
            #a = each.text.strip()
            #a = [x.replace("\r\n", " ") for x in a]
            #print(a)
            #player_array.append(each.text.strip())

        print(true_list)
        
        team_dict[player_name] = true_list
    # with open('soup3.csv', mode='w', encoding='utf-8', newline='') as employee_file:
    #                     employee_writer = csv.writer(employee_file)
    #                     employee_writer.writerow([team_dict])
    print(team_dict)
    return team_dict


#the real scraper used for all
def base_scraper(roster_url, site_url):
    #URL = 'https://seminoles.com/sports/basketball/roster/'
    #URL = "https://goduke.com/sports/mens-basketball/roster"
    #URL = 'https://rolltide.com/sports/football/roster'
    #URL = 'https://kuathletics.com/sports/mbball/roster/'
    #URL = 'https://baylorbears.com/sports/mens-basketball/roster'
    #URL = 'https://goaztecs.com/sports/mens-basketball/roster'
    #URL = 'https://gocards.com/sports/mens-basketball/roster'
    #URL = 'https://mgoblue.com/sports/mens-basketball/roster'
    print('in base scraper')

    #page = urllib.request.urlopen(roster_url)
    #print(page.read())
    #soup1 = BeautifulSoup(page.read(),'html.parser')

    #print(soup1)
    
    print('render')
   
    # try:
    #     result = asyncio.get_event_loop().run_until_complete(get_page(roster_url))
    # except Exception as err1:
    #     print(err1.message())
    # print(result)
    

    # result1 = get_url_async(roster_url)
   
   
    print('here done')
    


    base_url = roster_url
    sport = None
    try:
        print('attempt')
        sport = base_url.split('/')
        print(sport)
        if len(sport) > 4:
            sport=sport[4]
    except Exception as e:
        print(e.message())
        
    print(sport)

    #request the url

    #use headers to request from identity of an browser
    headers={}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    print('request')
    r = requests.get(roster_url, headers=headers)
    #except Exception as e:
        #print(e.message())
    print('request after')
    

    #scrape the entire web page
    soup = BeautifulSoup(r.content, 'html.parser')
    #print(soup)

    team_links = {}
    links= []
    #a2 = soup.find_all("td")
    #print(a2)
    #scrap the html id main-content
    a1 = soup.find_all("a", href=True)
    #a2 = soup1.find_all("a", href=True)
    print('')
    print('')
    print('after here')
    if a1 is None:
        print("a1 is None")
    #print(a1)
    result = a1
    not_normal_format=False

    print('before for loop')
    for link in result:
        print("")
        print("href: {}".format(link.get("href")))
        a = link.get("href")
        link_split = a.split('/')

        print(link_split)
        if 'roster' in link_split:
            print("here")
            print(str(sport))
            if str(sport) in link_split:
                #print("sport")
                if 'coaches' not in link_split:
                    if 'staff' not in link_split:
                        if 'coach' not in link_split:

                            #print(link_split)
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
                            links.append(a)
            else:
                  if 'coaches' not in link_split:
                      if 'staff' not in link_split:
                        if 'coach' not in link_split:

                            #print(link_split)
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
                            links.append(a)
        else:
            #check links split on 
            #illinoise did not include name in the url
            not_normal_format = True
            link_split=a.split()
            import re
            #print(link_split)
            #print(re.findall(r"[\w']+", a))
            link_split = re.findall(r"[\w']+", a)
            if "roster" in link_split:
                if "aspx" in link_split:
                    if "rp_id" in link_split:
                        team_links[a] = a
                        links.append(a)
           
            
    #print(team_links)
    #print(len(team_links))
    #print(team_links)
    # if len(team_links) == 0:
    #     try:
    #         team_dict = selenium_option(roster_url, sport, base_url)
    #     except Exception as error:
    #         pass
    # else:
    team_dict = find_items(team_links, site_url, not_normal_format)

    return team_dict

    #print(team_dict)

    #list of words to scrap for
    # wantedList=['parent','Parents', 'Father', 'Mother', 'father', 'mother', 'dad', 'Dad', 'Mom', 'mom', 'son of', 'Son of', 'daughter of', 'Daughter of']

    # returning_dict ={}

    # for key, value in team_dict.items():
    #     phrases_list = []

    #     for sentence_item in team_dict[key]:
    #         res = bool([ele for ele in wantedList if(ele in sentence_item)])
    #         if res:
    #             phrases_list.append(sentence_item)

    #     returning_dict[key] = phrases_list
    #print(returning_dict)

#base_scraper()

#sidearm-roster-players-container


#below are examples for reference
#url of dukes basketball team (works for Duke)
def bullet_points(url):
    URL = "https://goduke.com/sports/mens-basketball/roster"

    #request the url
    r = requests.get(URL)

    #scrape the entire web page
    soup = BeautifulSoup(r.content, 'html.parser')

    team_links = {}
    links= []

    #scrap the html id main-content
    a1 = soup.find(id="main-content")

    #list of words to scrap for
    wantedList=['parent','Parents', 'Father', 'Mother', 'father', 'mother', 'dad', 'Dad', 'Mom', 'mom', 'son of', 'Son of', 'daughter of', 'Daughter of']



    #find all the divs that include the class name
    result = a1.find_all('div', class_ = 'sidearm-list-card-details relative')


    """
    [ '/sports/mens-basketball/roster/wendell-moore-jr-/11776',
    '/sports/mens-basketball/roster/vernon-carey-jr-/11771',
    '/sports/mens-basketball/roster/cassius-stanley/11780',
    '/sports/mens-basketball/roster/tre-jones/11775',
    '/sports/mens-basketball/roster/javin-delaurier/11772',
    '/sports/mens-basketball/roster/joey-baker/11769',
    '/sports/mens-basketball/roster/jordan-goldwire/11773',
    '/sports/mens-basketball/roster/alex-o-connell/11777',
    '/sports/mens-basketball/roster/matthew-hurt/11774',
    '/sports/mens-basketball/roster/michael-savarino/11779',
    '/sports/mens-basketball/roster/jack-white/11781',
    '/sports/mens-basketball/roster/keenan-worthington/11782',
    '/sports/mens-basketball/roster/justin-robinson/11778',
    '/sports/mens-basketball/roster/mike-buckmire/11770']

    """



    #go throught the results
    for each in result:
        #print(len(result))
        link1 = each.find_all('a', href=True)
        for each1 in link1:
            a = each1['href'].split('/')
            #print(a)
            if 'coaches' not in a:
                player_name = a[4]
                team_links[player_name] = each1['href']
                links.append(each1['href'])

        #print(link1['href'])
        #links.append(link1['href'])
        #print(each)
        #print(" ")
        #print(" ")


    #print(links)
    #iterate through each player page
    team_dict = {}
    for key, value in team_links.items():
        player_dic = {}
        player_array=[]
        newURL = "https://goduke.com"+ value
        #print(newURL)
        new_r = requests.get(newURL)
        #print(new_r.text)
        new_soup = BeautifulSoup(new_r.content, 'html.parser')
        list_contents = new_soup.find_all("li")
        for each in list_contents:
            player_array.append(each.text.strip())
        team_dict[key] = player_array

        #print(player_array)
        #team_array.append(player_dic)

    #print(len(team_dict))

    returning_dict ={}

    for key, value in team_dict.items():
        phrases_list = []

        for sentence_item in team_dict[key]:
            res = bool([ele for ele in wantedList if(ele in sentence_item)])
            if res:
                phrases_list.append(sentence_item)

        returning_dict[key] = phrases_list


    #print(returning_dict)




def paragraph_scraper(url):
    URL = 'https://rolltide.com/sports/football/roster'


      #request the url
    r = requests.get(URL)

    #scrape the entire web page
    soup = BeautifulSoup(r.content, 'html.parser')

    team_links = {}
    links= []

    #scrap the html id main-content
    a1 = soup.find(id="main-content")

    #list of words to scrap for
    wantedList=['parent','Parents', 'Father', 'Mother', 'father', 'mother', 'dad', 'Dad', 'Mom', 'mom', 'son of', 'Son of', 'daughter of', 'Daughter of']



    #find all the divs that include the class name
    result = a1.find_all('div', class_ = 'sidearm-list-card-details relative')

    for each in result:
        #print(len(result))
        link1 = each.find_all('a', href=True)
        for each1 in link1:
            a = each1['href'].split('/')
            #print(a)
            if 'coaches' not in a:
                if 'staff' not in a:
                    player_name = a[4]
                    team_links[player_name] = each1['href']
                    links.append(each1['href'])

    print(links)

    team_dict = {}
    for key, value in team_links.items():
        player_dic = {}
        player_array=[]
        newURL = "https://rolltide.com"+ value
        #print(newURL)
        new_r = requests.get(newURL)
        #print(new_r.text)
        new_soup = BeautifulSoup(new_r.content, 'html.parser')
        list_contents = new_soup.find_all("p")
        for each in list_contents:
            player_array.append(each.text.strip())
        team_dict[key] = player_array
        #print("here")

        #print(player_array)
        #team_array.append(player_dic)

    print(len(team_dict))

    returning_dict ={}

    for key, value in team_dict.items():
        phrases_list = []

        for sentence_item in team_dict[key]:
            res = bool([ele for ele in wantedList if(ele in sentence_item)])
            if res:
                phrases_list.append(sentence_item)

        returning_dict[key] = phrases_list
    print(returning_dict)

#alabama_scraper()

def kansas_scraper():
    URL = 'https://kuathletics.com/sports/mbball/roster/'


      #request the url
    r = requests.get(URL)

    #scrape the entire web page
    soup = BeautifulSoup(r.content, 'html.parser')

    team_links = {}
    links= []

    #scrap the html id main-content
    a1 = soup.find(id="players")

    #list of words to scrap for
    wantedList=['parent','Parents', 'Father', 'Mother', 'father', 'mother', 'dad', 'Dad', 'Mom', 'mom', 'son of', 'Son of', 'daughter of', 'Daughter of']



    #find all the divs that include the class name
    result = a1.find_all('div', class_ = 'player')


    for each in result:
        #print(len(result))
        link1 = each.find_all('a', href=True)
        for each1 in link1:
            a = each1['href'].split('/')
            #print(a)
            if 'coaches' not in a:
                if 'staff' not in a:
                    player_name = a[len(a) - 2]
                    team_links[player_name] = each1['href']
                    links.append(each1['href'])

    print(team_links)
    print(len(team_links))

    team_dict = {}
    for key, value in team_links.items():
        player_dic = {}
        player_array=[]
        newURL = None
        if value[:5] == 'https':
            newURL = value
        else:
            newURL = "https://kuathletics.com"+ value
        #print(newURL)
        new_r = requests.get(newURL)
        #print(new_r.text)
        new_soup = BeautifulSoup(new_r.content, 'html.parser')
        list_contents = new_soup.find_all("p")
        for each in list_contents:
            player_array.append(each.text.strip())
        team_dict[key] = player_array

    print(len(team_dict))

    returning_dict ={}

    for key, value in team_dict.items():
        phrases_list = []

        for sentence_item in team_dict[key]:
            res = bool([ele for ele in wantedList if(ele in sentence_item)])
            if res:
                phrases_list.append(sentence_item)

        returning_dict[key] = phrases_list
    print(returning_dict)






def michigan_scraper():
    URL = "https://goduke.com/sports/mens-basketball/roster"

    #request the url
    r = requests.get(URL)

    #scrape the entire web page
    soup = BeautifulSoup(r.content, 'html.parser')

    team_links = {}
    links= []

    #scrap the html id main-content
    a1 = soup.find(id="main-content")

    #list of words to scrap for
    wantedList=['parent','Parents', 'Father', 'Mother', 'father', 'mother', 'dad', 'Dad', 'Mom', 'mom', 'son of', 'Son of', 'daughter of', 'Daughter of']

    #find all the divs that include the class name
    result = a1.find_all('div', class_ = 'sidearm-list-card-details relative')

    #go throught the results
    for each in result:
        #print(len(result))
        link1 = each.find_all('a', href=True)
        for each1 in link1:
            a = each1['href'].split('/')
            #print(a)
            if 'coaches' not in a:
                player_name = a[4]
                team_links[player_name] = each1['href']
                links.append(each1['href'])

        #print(link1['href'])
        #links.append(link1['href'])
        #print(each)
        #print(" ")
        #print(" ")


    #print(links)
    #iterate through each player page
    team_dict = {}
    for key, value in team_links.items():
        player_dic = {}
        player_array=[]
        bullet_array=[]
        if value[:5] == 'https':
            newURL = value
        else:
            newURL = base_url + value        
        #print(newURL)
        new_r = requests.get(newURL)
        #print(new_r.text)
        new_soup = BeautifulSoup(new_r.content, 'html.parser')

    print(len(team_dict))

    returning_dict ={}

    for key, value in team_dict.items():
        phrases_list = []

        for sentence_item in team_dict[key]:
            res = bool([ele for ele in wantedList if(ele in sentence_item)])
            if res:
                phrases_list.append(sentence_item)

        returning_dict[key] = phrases_list

        #list_contents = new_soup.find_all("li")



def roster_links(result):
    team_links = {}
    links= []

    for each in result:
        #print(len(result))
        link1 = each.find_all('a', href=True)
        for each1 in link1:
            a = each1['href'].split('/')
            #print(a)
            if 'coaches' not in a:
                if 'staff' not in a:
                    player_name = a[len(a)-2]
                    team_links[player_name] = each1['href']
                    links.append(each1['href'])

   






