import os
import sys
import requests
import pprint

apiKey="60BSELJ4STUEN8NZ"
pp = pprint.PrettyPrinter(indent=4)

def main():
	jsonObj={
	"apikey":apiKey,
	"function":"TIME_SERIES_DAILY_ADJUSTED",
	"symbol":"MSFT"
	}
	print(jsonObj)
	r = requests.get('https://www.alphavantage.co/query', jsonObj)
	r.status_code
	# print(r.json())
	pp.pprint(r.json())
	return
main()