# -*- coding: utf-8 -*-

import re
from datetime import datetime

def parse_url(url):
    """Returns type of legislation and  its ID.
    arguments:
    url - URL of legislation from Congress.gov	
    """
    url_parts = url.split('/')
    congress, chamber, billid = url_parts[4], url_parts[5], url_parts[6].split('?')[0]

    bill_type = ""

    if "senate-bill" in chamber:
        bill_type = "s"
    elif "house-bill" in chamber:
        bill_type = "hr"
    elif "senate-resolution" in chamber:
        bill_type = "sres"
    elif "house-resolution" in chamber:
        bill_type = "hres"
    elif "house-joint-resolution" in chamber:
        bill_type = "hjres"
    elif "senate-joint-resolution" in chamber:
        bill_type = "sjres"
    elif "house-concurrent-resolution" in chamber:
        bill_type = "hconres"
    elif "senate-concurrent-resolution" in chamber:
        bill_type = "sconres"
    else:
        bill_type = "notfound"

    
    full_billid = bill_type + billid
    congress_number = re.findall('\d+', congress)[0]

    return congress_number, full_billid

def find_urls(comment):
    """Returns URL found in Reddit comment.
    arguments:
    comment - Reddit comment to be searched for potential URLs
    """

    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', comment)

def format_comment_from_bill(bill):
    """Retuns string describing the legislation, formatted as a Reddit comment.
    arguments:
    bill - JSON object describing legislation obtained from Congress
    """
    newline = "  \n"

    comment = u"#\U0001F3DB **Here is some more information about [" + bill.bill + "](" + bill.congressdotgov_url + ")**" + (" - [PDF](" + bill.pdf + ")" + newline if len(bill.pdf) > 0 else "" + newline)

    comment = comment + "*****" + newline

    comment = comment + "######**" + bill.title + "**" + newline
    comment = comment + "***Subject:*** " + bill.primary_subject + newline
    comment = comment + "***Congress:*** " + bill.congress + newline
    comment = comment + "***Sponsor:*** " + bill.sponsor + " (" + bill.sponsor_party + "-" + bill.sponsor_state + ")" + newline
    comment = comment + "***Introduced:*** " + bill.introduced_date + newline
    comment = comment + "***Cosponsors:*** " + bill.cosponsors + newline

    comment = comment + "*****" + newline

    comment = comment + "***Committee(s):*** " + bill.committees + newline
    comment = comment + "***Latest Major Action:*** " + bill.latest_major_action_date + ". " + bill.latest_major_action + newline
    
    comment = comment + "*****" + newline

    comment = comment + "######**Versions**" + newline
    if len(bill.versions) == 0:
        comment = comment + "No versions were found for this bill." + newline
    else:
        comment = comment + "Status|Title" + newline
        comment = comment + ":--|:--" + newline
        for version in bill.versions:
            comment = comment + version.status + "|"
            comment = comment + version.title + newline

    comment = comment + "*****" + newline

    comment = comment + "######**Actions**" + newline
    if len(bill.actions) == 0:
        comment = comment + "No actions were found for this bill." + newline
    else:
        for action in bill.actions:
            comment = comment + datetime.strftime(action.date, '***%Y-%m-%d:*** ') + action.desc + newline
    
    comment = comment + "*****" + newline

    comment = comment + "######**Votes**" + newline
    if len(bill.votes) == 0:
        comment = comment + "No votes were found for this bill." + newline
    else:
        comment = comment + "Chamber|Date|Roll Call|Question|Yes|No|Didn't Vote|Result" + newline
        comment = comment + ":-:|:-:|:-:|:--|:-:|:-:|:-:|:-:" + newline
        for vote in bill.votes:
            comment = comment + vote.chamber + "|"
            comment = comment + datetime.strftime(vote.date, '%Y-%m-%d') + "|"
            comment = comment + vote.roll_call + "|"
            comment = comment + vote.question + "|"
            comment = comment + vote.total_yes + "|"
            comment = comment + vote.total_no + "|"
            comment = comment + vote.total_not_voting + "|"
            comment = comment + vote.result + newline

    comment = comment + "*****" + newline
    comment = comment + "[^^\[GitHub\]](https://github.com/kylefrost/Congress_Bill_Bot) ^^I ^^am ^^a ^^bot. [^^Feedback ^^is ^^welcome.](https://np.reddit.com/r/Congress_Bill_Bot)  ^^Created ^^by ^^/u/kylefrost"

    return comment
