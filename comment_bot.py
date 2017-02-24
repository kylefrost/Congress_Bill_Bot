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

for comment in reddit.subreddit('KyleFrost').stream.comments():
    urls = utils.find_urls(comment.body)

    if len(urls) > 0:
        for url in urls:
            url = url.replace(")", "")
            if "congress.gov/bill" not in url:
                continue
            
            congress, bill_id = utils.parse_url(url)

            reply = utils.format_comment_from_bill(pp.get_bill(congress, bill_id))

            comment.reply(reply)

            print "I replied to: " + comment.permalink()


    if "+/u/Congress_Bill_Bot [[" in comment.body:
        try:
            congress, bill_id = re.search(r'\[\[(.*?)\]\]', comment.body).group(1).lower().replace(" ", "").split(",")
        
            reply = utils.format_comment_from_bill(pp.get_bill(congress, bill_id))
        
            comment.reply(reply)
        
            print "I replied to: " + comment.permalink()
        except:
            comment.reply("Sorry, I couldn't seem to find that bill.")

        #print re.search(r'\[\[(.*?)\]\]').group(1).lower().replace(" ", "").split(",")
        #congress, bill_id = re.search(r'\[\[(.*?)\]\]').group(1).lower().replace(" ", "").split(",")
#
#        reply = utils.format_comment_from_bill(pp.get_bill(congress, bill_id))
#
#        comment.reply(reply)
#
#        print "I replied to: " + comment.permalink()
