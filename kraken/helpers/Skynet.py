#!/usr/bin/python

import time
from kraken.helpers.cURL import cURL
import sys
from kraken.all_settings.models import AlarmSetting
from kraken.database import db


class Skynet(object):

    debug = False
    base_url='http://skynet.local:3737/'
    device_name = 'KrakenMaster'
    device={}
    uuid='KRAKENMASTER5782123123' 
    token='123'
    curl=False

    def __init__(self, debug=False):
        " Constructor "
        self.debug = debug
        self.curl = cURL(debug=debug)
        if not self.get_skynet_info():
            self.register()
            if self.debug:
                print("Skynet info not saved yet")
        else:
            self.update_my_device({'online' : 'true'})
    
    def no_error(self, data):
        if data:
            if 'errors' in data:
                if self.debug:
                    print("Error Response %s " % data)
                print("Error for skynet request %s" % data['errors'])
            else:
                return True
        return False

    def get_skynet_status(self):
        print(self.base_url + 'status');
        data = self.curl.make_request(url=self.base_url + 'status')
        if self.no_error(data) and data['skynet'] == 'online':
            return True
        else:
            return False
    
    def get_skynet_info(self):
        token_model = AlarmSetting()
        token = token_model.get_pair('skynet_token')

        uuid_model = AlarmSetting()
        uuid = uuid_model.get_pair('skynet_uuid')

        if not uuid or not token:
            return False
        self.uuid = uuid.value
        self.token = token.value
        return {'uuid' : uuid.value, 'token' : token.value}

    def save_skynet_info(self, new_uuid, new_token):
        token_model = AlarmSetting()
        token = token_model.get_pair('skynet_token')

        if not token:
            token = token_model.create(name='skynet_token',
                            label='Skynet Token',
                            value=new_token)
        else:
            token = token.update(value=new_token)

        uuid_model = AlarmSetting()
        uuid = uuid_model.get_pair('skynet_uuid')

        if not uuid:
            uuid = uuid_model.create(name='skynet_uuid',
                            label='Skynet UUID',
                            value=new_uuid)
        else:
            uuid = uuid.update(value=new_uuid)
        self.uuid = uuid.value
        self.token = token.value

    def register(self):
        if not self.get_skynet_status():
            if self.debug:
                print("Skynet offline")
            return False
        #Delete All Devices with same shit
        args = {'name':self.device_name, 'group' : 'Kraken'}
        devices = self.search_devices()
        for device in devices:
            self.delete_device(device)
        data = self.curl.make_request(url=self.base_url + 'devices', method='POST', args=args)
        if self.debug and data:
            print("Register Data %s" % data)
        if self.no_error(data):
            if self.debug:
                print("Skynet Registered %s" % data['uuid'])
            self.save_skynet_info(data['uuid'], data['token'])
            return True
        return False
    
    def update_my_device(self, params):
        return self.update_device(self.uuid, params)

    def update_device(self, uuid, params):
        default = {'token':self.token}
        args = dict(default.items() + params.items())
        data = self.curl.make_request(url=self.base_url + 'devices/'+ uuid, method='PUT', args=args)
        if self.no_error(data):
            if self.debug:
                print("Skynet Device Updated %s" % data['uuid'])
            return True
        return False

    def get_device(self, uuid):
        data = self.curl.make_request(url=self.base_url + 'devices/' + uuid, method='GET')
        if self.no_error(data):
            if self.debug:
                print("Retrieved Device %s" % data)
            return data
        return False

    def send_message(self, devices="*", message={}):
        args = {"devices" : devices, "message" : message}
        data = self.curl.make_request(url=self.base_url + 'messages', method='POST', args=args, type_json=True)
        if self.no_error(data):
            if self.debug:
                print("Sent Message to Device(s) %s" % data)
            return data
        return False

    def search_devices(self, params={}):
        data = self.curl.make_request(url=self.base_url + 'devices', method='GET', args=params)
        if self.no_error(data):
            if self.debug:
                print("Search Devices %s" % data)
            return data
        return False

    def get_my_events(self):
        return self.get_events(self.uuid)
    
    def get_events(self, uuid):
        params = {'token' : self.token}
        data = self.curl.make_request(url=self.base_url + 'events/' + uuid, method='GET', args=params)
        if self.no_error(data):
            if self.debug:
                print("Retrieving Events %s" % data)
            return data
        return False
    
    def mysubscribe(self):
        return self.subscribe(self.uuid)

    
    def subscribe(self, uuid):
        params = {'token' : self.token}
        self.curl.make_request(url=self.base_url + 'subscribe/' + uuid, method='GET', args=params, streaming=True, callback=True)
        return True
    
    def delete_device(self, uuid):
        data = self.curl.make_request(url=self.base_url + 'devices/' + uuid, method='DELETE', args={'token' : self.token})
        if self.no_error(data):
            if self.debug:
                print("Delete Device %s" % data)
            return data
        return False
