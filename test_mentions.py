# -*- coding: utf-8 -*-

import const
import utils
import praw
import re
from propub import ProPublica

reddit = praw.Reddit(client_id=const.CLIENT_ID,
        client_secret=const.CLIENT_SECRET,
        user_agent=const.USER_AGENT,
        username=const.USERNAME,
        password=const.PASSWORD)

pp = ProPublica(const.PROPUB_KEY)

def bot():
    for mention in reddit.inbox.stream():
        if "+/u/congress_bill_bot" in mention.body.lower():
            print "************SUMMONED*************"

            try:
                congress, bill_id = re.search(r'\[\[(.*?)\]\]', comment.body).group(1).lower().replace(" ", "").replace(".", "").split(",")
            
                reply = utils.format_comment_from_bill(pp.get_bill(congress, bill_id))
            
                mention.reply(reply)
            
                print "I replied to: " + comment.permalink()
            except:
                comment.reply("Sorry, I couldn't seem to find that bill.")

while True:
    try:
        bot()
    except KeyboardInterrupt:
        pass
    except:
        pass
