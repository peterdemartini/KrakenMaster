#!/usr/bin/python

import time
import pycurl
import json
import urllib
from StringIO import StringIO

def recieve_messages(data):
    print("Awesomeness %s" % data)
    return False

class cURL(object):

    debug = False
    url=''
    method='GET'
    fields={}
    res=False
    c=False
    streaming=False
    callback=False

    def __init__(self, debug=False):
        " Constructor "
        self.debug = debug

    def make_request(self, url='', method='GET', args={}, type_json=False, streaming=False, callback=False):
        self.res = StringIO()
        if not type_json:
            self.fields = urllib.urlencode(args)
        else:
            self.fields = json.dumps(args, separators=(',',':'))

        if method == 'GET':
            self.url = ''.join([url, '?', self.fields])
        else:
            self.url = url
        self.method=method
        self.streaming=streaming

        if callback:
            self.callback = recieve_messages
        else:
            self.callback = self.res.write

        self.build()
        try:
            self.c.perform()
            if not streaming:
                self.c.close()
        except pycurl.error, error:
            errno, errstr = error
            print 'An error occurred: ', errstr
        #Return value
        val = self.res.getvalue();
        if val:
            return json.loads(val)
        else:
            return False

    def build(self):
        self.c = pycurl.Curl()
        if self.debug:
            print("URL :: %s " % self.url) 
        self.c.setopt(self.c.URL, str(self.url))
        if not self.streaming:
            self.c.setopt(self.c.CONNECTTIMEOUT, 5)
            self.c.setopt(self.c.TIMEOUT, 8)
        self.c.setopt(self.c.FAILONERROR, True)
        if self.method == 'POST':
            self.c.setopt(self.c.POSTFIELDS, self.fields)
        self.c.setopt(self.c.CUSTOMREQUEST, self.method)
        self.c.setopt(self.c.WRITEFUNCTION, self.callback)
