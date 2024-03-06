# Douban Short Comment Crawler

## Preparation
Before running, you have to login to douban and get the cookie and log in to wandb by ```wandb.login()```

- ```cookie.txt``` is a file to store the cookie of your douban account. Just simply copy the cookie from your browser and paste it into the file.

- ```douban_short_comment_by_moiveID.py``` is a python script to crawl short comments of a movie by its movie ID (you can find the movie ID in the URL of the movie page) divided into several csv files (Douban ranks short comments in several orders, i.e., 'all', 'good', 'normal', 'bad', 'watched_newest', 'wanna_watch_hotest', 'wanna_watch_newest').
- ```douban_short_comment_aggregation.py``` is a python script to aggregate the crawled comment csv files into one csv file.

## Comments Crwaling
Run the following command to get the short comments of a movie by its movie ID:

```python
python douban_short_comment_by_moiveID.py --movie_id <movie_id> --max_page <how many pages you wanna get> --cookie_location <cookie.txt's directory> --csv_dir <the folder's directory where you wanna save the  crawled comments>
```

## Comments Aggregation
Run the following command to aggregate the crawled comment csv files into 2 csv files (watched and wanna watch):

```python
python douban_short_comment_by_moiveID_agg.py --csv_dir <the folder's directory where you wanna save the  crawled comments> --agg_csv_dir <the folder's directory where you wanna save the  aggregated comments>
```

