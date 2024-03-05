
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import random
from time import sleep
from random import randint
import sys
import argparse
import wandb

parser = argparse.ArgumentParser(description='douban short comment crwaler arguments')
parser.add_argument('--movie_id', type=str, help='movie id of the movie you wanna crawl')
parser.add_argument('--max_page', type=int, help='max page of the movie comments you wanna crawl')
parser.add_argument('--cookie_location', type=str, help='cookie location of the login information')
parser.add_argument('--csv_dir', type=str, help='csv file directory to save the comments')
args = parser.parse_args()

movie_id = args.movie_id
max_page = args.max_page
cookie_location = args.cookie_location
csv_dir = args.csv_dir

wandb.init(project='douban_short_comment_crawler',config = args,reinit=True)
wandb.log({'movie_id': movie_id, 'csv_dir': csv_dir})

# Read the login cookie from a text file
with open(cookie_location, 'r') as f:
	cookie = f.read()

referer = 'https://movie.douban.com/subject/{}/comments?start=0&limit=20&status=P&sort=new_score'.format(movie_id)

h1 = {
	'Cookie': cookie,
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Host': 'movie.douban.com',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
	'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
	'Referer': referer,
	'Connection': 'keep-alive'
}


def trans_star(v_str):
	"""star converter to digits"""
	v_str = v_str[0]
	if v_str == 'allstar10':
		return '1'
	elif v_str == 'allstar20':
		return '2'
	elif v_str == 'allstar30':
		return '3'
	elif v_str == 'allstar40':
		return '4'
	elif v_str == 'allstar50':
		return '5'
	else:
		return 'unknown'


def get_short(v_movie_id):
	"""short comment crwaler"""
	for page in range(1, max_page + 1):  
		requests.packages.urllib3.disable_warnings()
		# url request
		url_all = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&status=P&sort=new_score'.format(v_movie_id, (page - 1) * 20)
			
		url_good = 'https://movie.douban.com/subject/{}/comments?percent_type=h&start={}&limit=20&status=P&sort=new_score'.format(v_movie_id, (page - 1) * 20)

		url_normal = "https://movie.douban.com/subject/{}/comments?percent_type=m&start={}&limit=20&status=P&sort=new_score".format(v_movie_id, (page - 1) * 20)

		url_bad = "https://movie.douban.com/subject/{}/comments?percent_type=l&start={}&limit=20&status=P&sort=new_score".format(v_movie_id, (page - 1) * 20)
		
		url_watched_newest = "https://movie.douban.com/subject/{}/comments?start={}&limit=20&status=P&sort=time".format(v_movie_id, (page - 1) * 20)

		url_wanna_watch_hotest = "https://movie.douban.com/subject/{}/comments?start={}&limit=20&status=F&sort=new_score".format(v_movie_id, (page - 1) * 20)

		url_wanna_watch_newest = "https://movie.douban.com/subject/{}/comments?start={}&limit=20&status=F&sort=time".format(v_movie_id, (page - 1) * 20)
		# get response
		url_list = [url_all, url_good, url_normal, url_bad, url_watched_newest, url_wanna_watch_hotest, url_wanna_watch_newest]
		url_type_list = ['all', 'good', 'normal', 'bad', 'watched_newest', 'wanna_watch_hotest', 'wanna_watch_newest']
		for url,url_type in zip(url_list, url_type_list):
			response = requests.get(url, headers=h1, verify=False)
			print(response.status_code)
			# parse html
			soup = BeautifulSoup(response.text, 'html.parser')
			# all comments
			reviews = soup.find_all('div', {'class': 'comment'})
			print('crawl page {} at {}, {} comments in total'.format(page, url_type, len(reviews)))
			sleep(randint(15,200))
			# empty list for saving
			user_name_list = []  # user alias
			star_list = []  # rating
			time_list = []  # comment time
			ip_list = []  # ip location
			vote_list = []  # vote number for useful
			content_list = []  # content
			for review in reviews:
				# user alias
				user_name = review.find('span', {'class': 'comment-info'}).find('a').text
				user_name_list.append(user_name)
				# rating
				star = review.find('span', {'class': 'comment-info'}).find_all('span')[1].get('class')
				star = trans_star(star)
				star_list.append(star)
				# comment time
				time2 = review.find('span', {'class': 'comment-time'}).text.strip()
				print('comment_time:', time2)
				time_list.append(time2)
				# ip location
				ip = review.find('span', {'class': 'comment-location'}).text
				ip_list.append(ip)
				# vote number for useful
				vote = review.find('span', {'class': 'votes vote-count'}).text
				vote_list.append(vote)
				# content
				content = review.find('span', {'class': 'short'}).text
				content = content.replace(',', '，').replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')
				content_list.append(content)
			df = pd.DataFrame(
				{
					'page_no': page,
					'commenter_alias': user_name_list,
					'comment_star': star_list,
					'comment_time': time_list,
					'commenter_IP': ip_list,
					'thumbs': vote_list,
					'comment_content': content_list,
				}
			)

			result_file = 'doubanMovie_{}_{}_{}pages.csv'.format(url_type,v_movie_id, max_page)
			# set header
			if os.path.exists(result_file):
				header = False
			else:
				header = True
			# save to csv
			
			df.to_csv(csv_dir+"/"+result_file, mode='a+', header=header, index=False, encoding='utf_8_sig')
			print('file saved successfully at {}{}'.format(csv_dir, result_file))
			# use wannd to log csv file name and save time
			wandb.log({url_type: result_file})
			wandb.log({url_type+'_saved_time': pd.Timestamp.now()})



if __name__ == '__main__':
	
	#movie_id = '35144311'
	# max page for crawling
	#max_page = 30 
	# result file name
	#result_file = 'doubanMovie_{}_{}pages.csv'.format(movie_id, max_page)
	# delete file if exists
	#if os.path.exists(result_file):
	#	os.remove(result_file)
	#	print('the files exists so delete this file: {}'.format(result_file))
	# circular crawling
	get_short(movie_id)
