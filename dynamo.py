import boto3

#name of the dynamoDB table
__TableName__ = "2ndGenSports"

client = boto3.client('dynamodb', region_name='us-east-1')

DB = boto3.resource('dynamodb', region_name='us-east-1')

#construct the appropriate table object based on __TableName__
table = DB.Table(__TableName__)

DEBUG = False

# method used to add an item into the database
def putItem(sport, teamName, year, count, keyWordCountDict, checkedList, resultsList, gender):

	print(sport)
	print(teamName)

	#checking if sport variable is a string
	if not (type(sport) == str):
		sport = str(sport)

	#checking if teamName variable is a string
	if not (type(teamName) == str):
		teamName = str(teamName)

	if not (type(gender) == str):
		gender = str(gender)

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

	if not (gender.islower()):
		gender = gender.lower()

	gender = gender.strip()



	#creating ID which is used to uniquely identify the data in the database
	ID = sport + teamName + str(year) + gender

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
			"Gender": gender
			,
			"Count": count 
			, 
			"parent": keyWordCountDict.get("parent", 0) 
			, 
			"parents": keyWordCountDict.get("parents", 0) 
			, 
			"father": keyWordCountDict.get("father", 0)   
			, 
			"mother": keyWordCountDict.get("mother", 0)  
			, 
			"dad": keyWordCountDict.get("dad", 0)  
			, 
			"mom": keyWordCountDict.get("mom", 0)  
			, 
			"son": keyWordCountDict.get("son", 0)  
			, 
			"daughter": keyWordCountDict.get("daughter", 0)  
			, 
			"checkedList": checkedList 
			, 
			"resultsList": resultsList
		}

	)

	if (DEBUG):
		print(response) 


def getItem(sport, teamName, year, gender):

	#checking if sport variable is a string
	if not (type(sport) == str):
		sport = str(sport)

	#checking if teamName variable is a string
	if not (type(teamName) == str):
		teamName = str(teamName)

	#checking if year variable is an int
	if not (type(year) == int):
		year = int(year)


	if not (type(gender) == str):
		gender = str(gender)


	#checking if sport and teamName are all lowercase and them of beginning and ending whitespace
	if not (sport.islower()):
		sport = sport.lower()

	sport = sport.strip()

	if not (teamName.islower()):
		teamName = teamName.lower()

	teamName = teamName.strip()


	if not (gender.islower()):
		gender = gender.lower()

	gender = gender.strip()


	#creating ID which is used to uniquely identify the data in the database
	ID = sport + teamName + str(year) + gender

	response = table.get_item(
		Key = {
			"ID": ID
		}
	)

	return response["Item"] 

def deleteItem(ID): 

	# #checking if sport variable is a string
	# if not (type(sport) == str):
	# 	sport = str(sport)

	# #checking if teamName variable is a string
	# if not (type(teamName) == str):
	# 	teamName = str(teamName)

	# #checking if year variable is an int
	# if not (type(year) == int):
	# 	year = int(year)


	# #checking if sport and teamName are all lowercase and them of beginning and ending whitespace
	# if not (sport.islower()):
	# 	sport = sport.lower()

	# sport = sport.strip()

	# if not (teamName.islower()):
	# 	teamName = teamName.lower()

	# teamName = teamName.strip()


	# #creating ID which is used to uniquely identify the data in the database
	# ID = sport + teamName + str(year) 

	response = table.delete_item( 
		Key = { 
			"ID" : ID 
		}
	) 

	if (DEBUG):
		print(response) 

def updateItem(sport, teamName, year, count, gender): 

	#checking if sport variable is a string
	if not (type(sport) == str):
		sport = str(sport)

	if not (type(gender) == str):
		gender = str(gender)

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


	if not (gender.islower()):
		gender = gender.lower()

	gender = gender.strip()



	#creating ID which is used to uniquely identify the data in the database
	ID = sport + teamName + str(year) + gender 

	response = table.update_item(
		Key = {
			"ID" : ID
		}, 
		UpdateExpression = "set #t = :i", 
		ExpressionAttributeValues = {
			':i' : count
		}, 
		ExpressionAttributeNames = { 
			"#t" : "Count"
		} 
	)

def getAllItems():

	response = table.scan() 

	return response["Items"]




if __name__ == '__main__':
	putItem("basketball", "duke", 2018, 8)
	print(getItem("basketball", "duke", 2018)) 
	#deleteItem("basketball", "duke", 2018) 
	updateItem("basketball", "duke", 2018, 20) 
	print(getItem("basketball", "duke", 2018))  
	print(getAllItems())
