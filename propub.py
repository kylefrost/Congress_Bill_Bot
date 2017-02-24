# -*- coding: utf-8 -*-

import requests
import errors as e
from datetime import datetime

class ProPublica(object):
    def __init__(self, apikey=None):
        self.apikey = apikey
        self.version = "1.0.0"
        self.base = "https://api.propublica.org/congress/v1/"

    def get(self, url):
        if self.apikey is None:
            raise e.UnauthorizedError('A ProPublica API key is required')

        headers = { 'X-API-Key' : self.apikey }
        return requests.get(url, headers=headers).json()

    def get_bill(self, congress, bill_id):
        url = self.base + congress + "/bills/" + bill_id + ".json"
        return Bill(self.get(url))

class Bill(object):
    def __init__(self, data=None):
        self.data = data

        if self.data is None:
            raise e.BillError('Unable to get bill data')

        if self.data['status'] != 'OK':
            raise e.BillError('There was a problem getting the bill data')

        self.bill_data = data['results'][0]

        # Put bill data into bill object

        self.congress = self.bill_data['congress']
        self.bill = self.bill_data['bill']
        self.bill_uri = self.bill_data['bill_uri']
        self.title = self.bill_data['title']
        self.sponsor = self.bill_data['sponsor']
        self.sponsor_uri = self.bill_data['sponsor_uri']
        self.pdf = self.bill_data['gpo_pdf_uri']
        self.introduced_date = self.bill_data['introduced_date']
        self.cosponsors = self.bill_data['cosponsors']
        self.primary_subject = self.bill_data['primary_subject']
        self.committees = self.bill_data['committees']
        self.latest_major_action_date = self.bill_data['latest_major_action_date']
        self.latest_major_action = self.bill_data['latest_major_action']
        self.house_passage_vote = self.bill_data['house_passage_vote']
        self.senate_passage_vote = self.bill_data['senate_passage_vote']
        
        self.versions = []
        i = 0
        for version in self.bill_data['versions']:
            self.versions.append(Map(status=version['status'], title=version['title'], url=version['thomas_url']))
            i = i + 1

        self.actions = []
        i = 0
        for action in self.bill_data['actions']:
            self.actions.append(Map(date=datetime.strptime(action['datetime'][:10], '%Y-%m-%d'), desc=action['description']))
            i = i + 1

        self.votes = []
        i = 0
        for vote in self.bill_data['votes']:
            self.votes.append(Map(chamber=vote['chamber'],
                date=datetime.strptime(vote['date'], '%Y-%m-%d'),
                time=datetime.strptime(vote['time'], '%H:%M'),
                roll_call=vote['roll_call'],
                question=vote['question'],
                result=vote['result'],
                total_yes=vote['total_yes'],
                total_no=vote['total_no'],
                total_not_voting=vote['total_not_voting'],
                api_url=vote['api_url']))
            i = i + 1

class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]
