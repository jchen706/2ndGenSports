import boto3

#name of the dynamoDB table
__TableName__ = "2ndGenSports"

client = boto3.client('dynamodb', region_name='us-east-1')

DB = boto3.resource('dynamodb', region_name='us-east-1')

#construct the appropriate table object based on __TableName__
table = DB.Table(__TableName__)

DEBUG = False

# method used to add an item into the database
def putItem(sport, teamName, year, count):

	#checking if sport variable is a string
	if not (type(sport) == str):
		sport = str(sport)

	#checking if teamName variable is a string
	if not (type(teamName) == str):
		teamName = str(teamName)

	#checking if year variable is an int
	if not (type(year) == int):
		year = int(year)

	#checking if count variable is an int
	if not (type(count) == int):
		count = int(count)


	#checking if sport and teamName are all lowercase and them of beginning and ending whitespace
	if not (sport.islower()):
		sport = sport.lower()

	sport = sport.strip()

	if not (teamName.islower()):
		teamName = teamName.lower()

	teamName = teamName.strip()


	#creating ID which is used to uniquely identify the data in the database
	ID = sport + teamName + str(year)

	#calling put_item method on the table which takes a dictionary as its parameter. The dictionary maps table column name(str) to value.
	response = table.put_item(
		Item = {
			"ID": ID
			,
			"Sport": sport
			,
			"TeamName": teamName
			,
			"Year": year
			,
			"Count": count
		}
	)

	if (DEBUG):
		print(response)

def getItem(sport, teamName, year):

	#checking if sport variable is a string
	if not (type(sport) == str):
		sport = str(sport)

	#checking if teamName variable is a string
	if not (type(teamName) == str):
		teamName = str(teamName)

	#checking if year variable is an int
	if not (type(year) == int):
		year = int(year)


	#checking if sport and teamName are all lowercase and them of beginning and ending whitespace
	if not (sport.islower()):
		sport = sport.lower()

	sport = sport.strip()

	if not (teamName.islower()):
		teamName = teamName.lower()

	teamName = teamName.strip()


	#creating ID which is used to uniquely identify the data in the database
	ID = sport + teamName + str(year)

	response = table.get_item(
		Key = {
			"ID": ID
		}
	)

	return response["Item"]



if __name__ == '__main__':
	putItem("basketball", "duke", 2018, 8)
	print(getItem("basketball", "duke", 2018))