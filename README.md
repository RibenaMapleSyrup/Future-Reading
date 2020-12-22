# Future-Reading
These scripts marked the beginning of me playing around with Reddit data.

For my first attempt at exploring the history of a subreddit, I was curious to map the dates mentioned within articles shared in r/futurology over the past decade.
Big thanks to [Stuck-In-The-Matrix](https://www.reddit.com/r/pushshift/comments/89pxra/pushshift_api_with_large_amounts_of_data/dwuqgf6) for the reddit-scraping code and [PH01L](https://github.com/osrsbox) for the [great article](https://www.osrsbox.com/blog/2019/03/17/data-is-beautiful-6-year-analysis-of-reddit-2007scape/) on scraping /r/2007scape!

'subreddit_scrape.py' can be used to grab submissions to any subreddit between two dates in time and write them to a new JSON file. To run the script: 
```python3 subreddit_scrape.py --start <YYYYMMDD> --end <YYYYMMDD> --filename <filename-without-extension> --subreddit <name-of-chosen-subreddit>```

For instance if we wanted to scrape all of the submissions to r/futurology over the course of 2020, and save them to a file called 'endOftheFuture.json' we would run: 
```python3 subreddit_scrape.py --start 20200101 --end 20201231 --filename endOftheFuture --subreddit futurology```
