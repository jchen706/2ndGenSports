import requests
from bs4 import BeautifulSoup

#gets the rankings from ESPN
#Works just need to connected to user interface
def espnscraper(base_url):

    
    #request the url
    r = requests.get(base_url)

    #scrape the entire web page
    soup = BeautifulSoup(r.content, 'html.parser')

    data = []
    table = soup.find('table', attrs={'class': "Table"})
    print(table)
    table_body = table.find('tbody')
    print(table_body)


    rows = table_body.find_all('tr')
    dictionary1 = {}
    for row in rows:
        print(row)
        #print(len(row))
    
       
        cols = row.find_all('td')
        #print(cols)
        print(cols[0])
        rankings = cols[0].text.strip()
        #print()
        #print(cols[1])
        team_name = cols[1].find_all('a')[-1].text.strip()
        dictionary1[rankings]= team_name
        #print(team_name)
        #print(cols)
        #dictionary1[cols[1].text.strip()]

        #cols = [ele.text.strip() for ele in cols]
        #data.append([ele for ele in cols if ele])
    # print(data)

    # for i in range(len(data)):
    #     for k in range(len(data[i][1])):
    #         if data[i][1][k] == data[i][1][k].lower():
    #             data[i][1] = data[i][1][k-1] + data[i][1][k:]
    #             break
    
    # print(data)
    print(dictionary1)




    #class= Table

  
#espnscraper('https://www.espn.com/mens-college-basketball/rankings/_/year/2018')
