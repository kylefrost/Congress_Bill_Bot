# -*- coding: utf-8 -*-

import const
import utils
import praw
import sys
from propub import ProPublica

reddit = praw.Reddit(client_id=const.CLIENT_ID,
        client_secret=const.CLIENT_SECRET,
        user_agent=const.USER_AGENT,
        username=const.USERNAME,
        password=const.PASSWORD)

pp = ProPublica(const.PROPUB_KEY)

def bot():
    for submission in reddit.subreddit(sys.argv[1]).stream.submissions():
        if "congress.gov/bill" not in submission.url:
            continue

        congress, bill_id = utils.parse_url(submission.url)

        try:
            comment = utils.format_comment_from_bill(pp.get_bill(congress, bill_id))

            submission.reply(comment)
            
            print "I replied to: " + submission.shortlink
        except:
            pass

while True:
    try:
        bot()
    except KeyboardInterrupt:
        break
