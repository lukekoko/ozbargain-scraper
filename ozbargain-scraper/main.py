from config import config
import logging
from scraper import Scraper
from notifications import Notifications
from sql import SQL
import time
import sys

def main():
	logging.config.fileConfig(config.settings['logger-config'], disable_existing_loggers=False)
	logger = logging.getLogger(__name__)
	while True:
		try:
			with Scraper() as scrape:
				nots = Notifications()
				rawData = scrape.fetchData(0, 5)
				extractedData = scrape.extractData(rawData)
				with SQL() as sql:
					sql.insertIntoSQL(extractedData)
				for i in scrape.searchDeals(extractedData):
					nots.sendSMS(i)
			logger.debug('Waiting...')
			time.sleep(300)
		except KeyboardInterrupt:
			logging.debug('Exiting...')
			sys.exit(0)

if __name__ == "__main__":
	main()