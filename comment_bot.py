# -*- coding: utf-8 -*-

import const
import utils
import praw
import re
import sys
from propub import ProPublica

reddit = praw.Reddit(client_id=const.CLIENT_ID,
        client_secret=const.CLIENT_SECRET,
        user_agent=const.USER_AGENT,
        username=const.USERNAME,
        password=const.PASSWORD)

pp = ProPublica(const.PROPUB_KEY)

def bot():
    for comment in reddit.subreddit(sys.argv[1]).stream.comments():
        urls = utils.find_urls(comment.body)

        if len(urls) > 0:
            bills = []


            for url in urls:
                url = url.replace(")", "")
                if "congress.gov/bill" not in url:
                    continue


                print "\n***************URL*****************"
                print "Working on comment: " + comment.permalink(fast=True)

                print "Working on: " + url
                congress, bill_id = utils.parse_url(url)

                print "Found Congress: " + congress + ", and Bill: " + bill_id

                print "Adding bill to list."
                bill = pp.get_bill(congress, bill_id)
                print "Got Bill titled: " + bill.title

                bills.append(bill)

            if len(bills) > 0:
                print "---------- Working on Bills! ----------"
                reply = ""
                for bill in bills:
                    print "Adding bill to reply: " + bill.title
                    reply = reply + "  \n*****  \n" + utils.format_comment_from_bill(bill)

                comment.reply(reply)
                print "I replied to: https://reddit.com" + comment.permalink()

        elif "+/u/Congress_Bill_Bot [[" in comment.body:
            print "************SUMMONED*************"
            print "Comment: " + comment.permalink(fast=True)

            try:
                congress, bill_id = re.search(r'\[\[(.*?)\]\]', comment.body).group(1).lower().replace(" ", "").replace(".", "").split(",")
            
                reply = utils.format_comment_from_bill(pp.get_bill(congress, bill_id))
            
                comment.reply(reply)
            
                print "I replied to: " + comment.permalink()
            except:
                comment.reply("Sorry, I couldn't seem to find that bill.")


while True:
    try:
        bot()
    except KeyboardInterrupt:
        exit()
    except:
        pass
