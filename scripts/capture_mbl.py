import os
import imp
import tqdm
import dask
import sqlite3
from dateutil import rrule
from datetime import datetime, timedelta
tw = imp.load_source('tw', '../twitter-past-crawler/src/twitterpastcrawler/crawler.py')


def generate_queries(since, until):

	dates = list(rrule.rrule(rrule.WEEKLY,
							 dtstart=since, 
							 until=until))

	dates  = map(lambda x: [datetime.strftime(y, "%Y-%m-%d") for y in x], 
						zip(dates[:-1], dates[1:]))

	base_url = 'https://twitter.com/i/search/timeline?l=&q='
	param = '&vertical=default&max_position=hoge&src=typd&include_entities=1&include_available_features=1'
	
	queries = ['from%3Amblivre%20since%3A{since}%20until%3A{until}'.format(
																since=dt[0],
																until=dt[1]) 
															for dt in dates]

	queries = [''.join([base_url, query, param]) for query in queries]

	return queries

def capture(name='mbl',
			lang='pt',
			force_reset=False):

	db = sqlite3.connect('tweets')
	cursor = db.cursor()

	until = datetime.now()
	since = datetime.strptime('2013/06/01', '%Y/%m/%d')

	queries = generate_queries(since=since, until=until)

	for query in tqdm.tqdm(queries):

		print(query)
		
		crawler = tw.TwitterCrawler(
									query=query, 
									name=name,
									lang=lang,
									force_reset=force_reset,
									output_file="tweets" 
								)

		crawler.crawl()

		cursor.execute('SELECT COUNT(*) FROM tweets_{}'.format(name))
		print(cursor.fetchone())

	db.close()

def main():
	pass

if __name__ == '__main__':
	capture()