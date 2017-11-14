import csv
import requests
import random
import string
import sys
import time
import xml.etree.ElementTree as ET

# Random factors:
#
#   1. Time between quote requests.
#   2. Ticker symbol.
#   3. Online quote provider (ie, URL).
#
# For (2) and (3), we just use the built-in RNG with a uniform distribution.
# For (1), we want a "bursty" distribution, so we rely on a Poisson distribution
# to determine when to fire the next quote request.

# Average time between quote queries, in seconds.
mean_time_between_quotes = 10.0

ticker_symbols = []
user_agents = []
brokerage_quote_urls = [
	'http://www.morningstar.com/stocks/xnys/{0}/quote.html',
	'http://www.wikinvest.com/wiki/{0}',
	'https://www.barchart.com/stocks/quotes/{0}',
	'http://www.foxbusiness.com/quote.html?stockTicker={0}',
	'https://www.msn.com/en-us/money/stockdetails/{0}',
	'https://www.advfn.com/stock-market/NYSE/{0}/stock-price',
	'https://www.macroaxis.com/invest/market/{0}',
	'https://www.cnbc.com/quotes/?symbol={0}',
	'https://finviz.com/quote.ashx?t={0}',
	'https://finance.google.com/finance?q={0}',
	'http://www.nasdaq.com/symbol/{0}',
	'https://finance.yahoo.com/quote/{0}',
	'https://www.marketwatch.com/investing/stock/{0}',
	'http://quotes.wsj.com/{0}',
	'https://seekingalpha.com/symbol/{0}',
	'https://www.thestreet.com/quote/{0}.html',
	'http://www.reuters.com/finance/stocks/overview/{0}',
	'http://money.cnn.com/quote/quote.html?symb={0}',
	'https://www.bloomberg.com/quote/{0}:US',
	'https://www.investopedia.com/markets/stocks/{0}',
	'http://caps.fool.com/Ticker/{0}.aspx',
	'https://www.zacks.com/stock/quote/{0}',
	'http://www.investorguide.com/stock.php?ticker={0}',
	'https://research.scottrade.com/qnr/public/Stocks/Snapshot?lang=EN&symbol={0}'
]

def main():
	# Read ticker symbols.
	with open("nasdaqtraded.txt", "rb") as csvfile:
		ticker_reader = csv.reader(csvfile, delimiter="|")
		next(ticker_reader, None)

		for ticker_row in ticker_reader:
			ticker_symbols.append(ticker_row[1])

	# Read user agents.
	user_agents_tree = ET.parse("user-agents.xml")
	for target in user_agents_tree.findall(".//folder//useragent"):
		user_agents.append(target.get("useragent"))

	fmt = string.Formatter()
	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'en-US,en;q=0.8',
	}

	print("Starting quote queries:")
	quote_query_count = 0
	while True:
		# Get random user-agent.
		user_agent_idx = random.randint(0, len(user_agents)-1)
		headers['User-Agent'] = user_agents[user_agent_idx]

		# Get random ticker symbol.
		ticker_idx = random.randint(0, len(ticker_symbols)-1)
		ticker = ticker_symbols[ticker_idx]

		# Get random online quote provider.
		quote_provider_idx = random.randint(0, len(brokerage_quote_urls)-1)
		quote_provider = brokerage_quote_urls[quote_provider_idx]

		# Make the quote request.
		quote_url = fmt.format(quote_provider, ticker)
		try:
			requests.get(quote_url, headers=headers)
			quote_query_count += 1
			print '.',
			sys.stdout.softspace=False
		except requests.exceptions.ConnectionError:
			continue

		if (quote_query_count % 5) == 0:
			print(fmt.format(" Number of queries: {0}", quote_query_count))

		# Wait DELAY seconds before making the next quote request.
		delay = random.expovariate(1.0 / mean_time_between_quotes)
		time.sleep(delay)

if __name__ == "__main__":
	main()
