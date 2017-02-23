# -*- coding: utf-8 -*-

import const
import praw
from propub import ProPublica

reddit = praw.Reddit(client_id=const.CLIENT_ID,
        client_secret=const.CLIENT_SECRET,
        user_agent=const.USER_AGENT,
        username=const.USERNAME,
        password=const.PASSWORD)

pp = ProPublica(const.PROPUB_KEY)

bill = pp.get_bill('115', 'hr38')

print bill

#for comment in reddit.subreddit('KyleFrost').stream.comments():
#    print comment.body
