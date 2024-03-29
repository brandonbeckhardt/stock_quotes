import os
import sys
import requests
import pprint
# from airtable-python-wrapper import Airtable
from airtable import Airtable
from datetime import date
import json

apiKey="60BSELJ4STUEN8NZ"
pp = pprint.PrettyPrinter(indent=4)


def main():
	airtable = Airtable('appLWRsE1SsJOsoOP', 'patrbEJ15TfKSNTnV.967e25a5f15e776d9df8865a0d6724ba4e172d029a71f7bc43d7a8125fd05a51')
	airtable.get('Current Holdings')
	# airtable.get_all()
	# holdings = airtable.get_all(formula="Symbol")
	holdings = airtable.get('Current Holdings')['records']
	print(holdings)

	assetIdData={}
	with open('cryptoApiAssets.txt') as json_file:
	    assetIdData = json.load(json_file)['payload']
	usdCryptoId = ""
	for assetIdDict in assetIdData:
		if assetIdDict['originalSymbol'] == "USD":
			usdCryptoId=assetIdDict["_id"]
			break


	for holding in holdings:
		if 'Symbol' in holding['fields']:
			symbol = holding['fields']['Symbol'][0]
			assetTypeExists=True
			if symbol!='USD':
				if 'Asset Type' not in holding['fields']:
					print("No asset type for " + symbol)
					assetTypeExists=False
				if assetTypeExists==False or "Crypto" not in holding['fields']['Asset Type'][0]:
					getNonCryptoInfo(holding, symbol, airtable)
				else:
					getCryptoInfo(holding, symbol, airtable, assetIdData, usdCryptoId)
	return

def getNonCryptoInfo(holding, symbol, airtable):
	r = requests.get("https://sandbox.tradier.com/v1/markets/quotes",
		{"symbols":symbol},
	  headers={
	    "Accept":"application/json",
         "Authorization":"Bearer fr0EicWidzcRf3RAPzCmGNQJKezf"
 	 	}
	)
	if 'quote' in r.json()['quotes']:
		# print(r.json())
		quoteInfo=r.json()['quotes']['quote']
		recentAskPrice = quoteInfo['ask']
		print(symbol + " - " + str(recentAskPrice))
		updateAirtableMostRecentPrice(airtable, holding, recentAskPrice)
	else:
		print("Unable to get quote for " + symbol)

def getCryptoInfo(holding, symbol, airtable, assetIdData, usdCryptoId):
	for assetIdDict in assetIdData:
		if assetIdDict['originalSymbol'] == symbol:
			idToSearch = assetIdDict["_id"]
			r = requests.get('https://api.cryptoapis.io/v1/exchange-rates/'+idToSearch+'/'+usdCryptoId,
  				headers={
   					"X-API-Key": "6619ad586520a48ccf978403e1a0498343bd9c71",
   					"Content-Type": "application/json"
	 				}
			)
			if 'payload' in r.json():
				recentPrice = r.json()['payload']['weightedAveragePrice']
				print(symbol + " - " + str(recentPrice))
				updateAirtableMostRecentPrice(airtable, holding, recentPrice)
			else:
				print("Could not find payload for " + symbol)
				print(r.json())

def updateAirtableMostRecentPrice(airtable, holding, recentPrice):
	recordId=holding['id']
	fields={'Most Recent Price': recentPrice, 'Most Recent Price Update Date':date.today().strftime("%B %d, %Y") }
	airtable.update('Current Holdings',recordId, fields)

main()
