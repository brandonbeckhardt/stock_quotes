import os
import sys
import requests
import pprint
# from airtable-python-wrapper import Airtable
from airtable import Airtable
import unirest

apiKey="60BSELJ4STUEN8NZ"
pp = pprint.PrettyPrinter(indent=4)




def main():


	airtable = Airtable('appLWRsE1SsJOsoOP', 'Current Holdings',api_key='keyOFzjy926o6Hx04')
	airtable.get_all()
	holdings = airtable.get_all(formula="Symbol")

	for holding in holdings:
		
		symbol = holding['fields']['Symbol'][0]
		# print(jsonObj)
		
		r = requests.get("https://sandbox.tradier.com/v1/markets/quotes",
			{"symbols":symbol},
		  headers={
		    "Accept":"application/json",
	         "Authorization":"Bearer fr0EicWidzcRf3RAPzCmGNQJKezf"
	 	 	}
		)
		quoteInfo=r.json()['quotes']['quote']
		recentAskPrice = quoteInfo['ask']
		recordId=holding['id']
		print("Symbol: " + symbol + " - Ask Price: " + str(recentAskPrice))
		fields={'Most Recent Price': recentAskPrice}
		airtable.update(recordId, fields)
	return
main()