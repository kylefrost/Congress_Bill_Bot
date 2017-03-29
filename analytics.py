import MySQLdb
import const
import datetime

def db_insert(bill, author, sub, post_t):
    chamber = bill.bill[:1]
    billid = int(filter(str.isdigit, str(bill.bill)))
    billtype = ""
    if bill.bill_type == "hr" or bill.bill_type == "s":
        billtype = "bill"
    elif bill.bill_type == "hres" or bill.bill_type == "sres":
        billtype = "res"
    elif bill.bill_type == "hjres" or bill.bill_type == "sjres":
        billtype = "jres"
    elif bill.bill_type == "hconres" or bill.bill_type == "sconres":
        billtype = "conres"
    congress = int(bill.congress)
    link_author = "/u/" + author
    subreddit = "/r/" + sub.display_name
    date_linked = datetime.datetime.today().strftime('%Y-%m-%d')
    post_type = post_t

    db = MySQLdb.connect(host="localhost", user=const.SQL_USER, passwd=const.SQL_PASS, db="congress_bill_bot")

    cursor = db.cursor()

    try:
        cursor.execute("INSERT INTO bills (chamber, billid, billtype, congress, link_author, subreddit, date_linked, post_type) VALUES('%s', %d, '%s', %d, '%s', '%s', '%s', '%s')" % (chamber, billid, billtype, congress, link_author, subreddit, date_linked, post_type))
        db.commit()
    except Exception as e:
        print "could not insert", e.message
        db.rollback()

    cursor.close()
