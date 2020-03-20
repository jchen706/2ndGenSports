import requests
from bs4 import BeautifulSoup

#url of dukes basketball team
URL = "https://goduke.com/sports/mens-basketball/roster"

#request the url
r = requests.get(URL)

#scrape the entire web page
soup = BeautifulSoup(r.content, 'html.parser')


links= []

#scrap the html id main-content
a1 = soup.find(id="main-content")


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
        if 'coaches' not in a:
            links.append(each1['href'])
    
    #print(link1['href'])
    #links.append(link1['href'])
    #print(each)
    #print(" ")
    #print(" ")


print(links)
#iterate through each player page
team_array = []
for eachPlayerLink in links:
    player_array=[]
    newURL = "https://goduke.com"+ eachPlayerLink
    #print(newURL)
    new_r = requests.get(newURL)
    #print(new_r.text)
    new_soup = BeautifulSoup(new_r.content, 'html.parser')
    list_contents = new_soup.find_all("li")
    for each in list_contents:
        player_array.append(each.text.strip())

    #print(player_array)
    team_array.append(player_array)

print(len(team_array))









#table = soup.find('a', attrs = {'class':'sidearm-sports-file-link-read sidearm-sports-file-link-processed'})
#
# table2 = soup.find('tr', class2_ = 'odd')

#print(a1.prettify())

#print(soup.prettify)
