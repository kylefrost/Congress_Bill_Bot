# -*- coding: utf-8 -*-

import const
import utils
import praw

reddit = praw.Reddit(client_id=const.CLIENT_ID,
        client_secret=const.CLIENT_SECRET,
        user_agent=const.USER_AGENT,
        username=const.USERNAME,
        password=const.PASSWORD)

def bot():
    try:
        for comment in reddit.subreddit().stream.comments():
            try:
                urls = utils.find_urls(comment.body)

                if len(urls) > 0:
                    for url in urls:
                        url = url.replace(")", "")
                        if "congress.gov/bill" not in url:
                            continue

                        print comment.permalink()
            except:
                pass
    except:
        pass

while True:
    bot()
