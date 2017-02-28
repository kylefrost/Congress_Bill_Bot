# -*- coding: utf-8 -*-

import const
import praw

reddit = praw.Reddit(client_id=const.CLIENT_ID,
        client_secret=const.CLIENT_SECRET,
        user_agent=const.USER_AGENT,
        username=const.USERNAME,
        password=const.PASSWORD)


def bot():
    try:
        for submission in reddit.subreddit('all').stream.submissions():
            if "congress.gov/bill" not in submission.url:
                continue

            print submission.shortlink
    except:
        pass

while True:
    bot()
