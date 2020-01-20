import boto3 

__TableName__ = "2ndGen" 

client = boto3.client('dynamodb') 

DB = boto3.resource('dynamodb') 

table = DB.Table(__TableName__)  

aString = "hello"

def getItem():

	response = table.get_item(
		Key = {
			"UserId": "Bob"
		} 
	) 
	
	print(response["Item"]) 

def putItem():
	
	response = table.put_item(  
		Item = {
			"UserId":"Phillip"
			, 
			"Age": '20'
			, 
			"Height": '44'
			, 
			"Income": '20'
		}
	)  
	print(response) 

def deleteItem():
	response = table.delete_item(
		Key = {
			"UserId" : "Phillip"
		} 
	) 

def updateItem():
	response = table.update_item(
		Key = {
			"UserId" : "Phillip"
		}, 
		UpdateExpression = "set Income = :i", 
		ExpressionAttributeValues = {
			':i' : 2000
		} 


		# AttributeUpdates = {
		# 	"Income": '2000'
		# } 
	)
def printHi():
	print(aString) 


 
if __name__ == '__main__': 
	# getItem() 
	# putItem() 
	# deleteItem()
	# updateItem() 

	print('this is the main method')
