import requests
from bs4 import BeautifulSoup

#find the items of paragraph or list in the player's page
def find_items(team_links, base_url):
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

        list_contents = new_soup.find_all("p")

        #list_contents = new_soup.find_all("li")



        for each in list_contents:
            a = each.text.strip()
            #a = [x.replace("\r\n", " ") for x in a]
            print(a)
            player_array.append(each.text.strip())



        team_dict[key] = player_array
    return team_dict


#sidearm-roster-players-container

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


#only can be run with paragraphs
def base_scraper():
    #URL = 'https://seminoles.com/sports/basketball/roster/'
    #URL = "https://goduke.com/sports/mens-basketball/roster"
    #URL = 'https://rolltide.com/sports/football/roster'
    #URL = 'https://kuathletics.com/sports/mbball/roster/'
    #URL = 'https://baylorbears.com/sports/mens-basketball/roster'
    URL = 'https://goaztecs.com/sports/mens-basketball/roster'
    URL = 'https://gocards.com/sports/mens-basketball/roster'
    URL = 'https://mgoblue.com/sports/mens-basketball/roster'

    base_url = URL
    sport = base_url.split('/')[4]
    #print(sport)

    #request the url
    r = requests.get(URL)

    #scrape the entire web page
    soup = BeautifulSoup(r.content, 'html.parser')

    team_links = {}
    links= []

    #scrap the html id main-content
    a1 = soup.find_all("a", href=True)
    #print(a1)
    result = a1


    for link in result:
        #print("")
        #print("href: {}".format(link.get("href")))
        a = link.get("href")
        link_split = a.split('/')

        print(link_split)
        if 'roster' in link_split:
            # print("here")
            #print(str(sport))
            if str(sport) in link_split:
                #print("sport")
                if 'coaches' not in link_split:
                    if 'staff' not in link_split:
                        if 'coach' not in link_split:

                            #print(link_split)
                            #print(a)
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
    print(team_links)
    print(len(team_links))

    team_dict = find_items_michigan(team_links, 'https://mgoblue.com')

    print(team_dict)

    #list of words to scrap for
    wantedList=['parent','Parents', 'Father', 'Mother', 'father', 'mother', 'dad', 'Dad', 'Mom', 'mom', 'son of', 'Son of', 'daughter of', 'Daughter of']

    returning_dict ={}

    for key, value in team_dict.items():
        phrases_list = []

        for sentence_item in team_dict[key]:
            res = bool([ele for ele in wantedList if(ele in sentence_item)])
            if res:
                phrases_list.append(sentence_item)

        returning_dict[key] = phrases_list
    print(returning_dict)

#base_scraper()



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

   






