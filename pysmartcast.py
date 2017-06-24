import json
import logging
import requests
import time
import warnings

class SmartCast(object):
    """
    Interact with a Vizio SmartCast TV using the Network API
    """
    
    def __init__(self, host, key, port=9000):
        self.host = host
        self.port = port
        self.key = key
        self.ssl_verify = False
        
        self.url = 'https://' + host + ':' + str(port) + '/'
        
        if self.ssl_verify is False:
            warnings.simplefilter("default", category=requests.packages.
                                  urllib3.exceptions.InsecureRequestWarning)
                                  
        self.session = requests.Session()
        self.session.verify = self.ssl_verify
        
        self.session.headers.update({'AUTH':self.key})
    
    def getPowerStatus(self):
        """
        Get the current on/off status of the device
        """
        url = self.url + 'state/device/power_mode'
        response = self.session.get(url)
        data = json.loads(response.text)
        return data['ITEMS'][0]['VALUE']
    
    def getInputs(self):
        """
        Returns all available inputs on the device
        """
        url = self.url + 'menu_native/dynamic/tv_settings/devices/name_input'
        response = self.session.get(url);
        inputs = json.loads(response.text)['ITEMS']
        return inputs
        
    def getActiveInput(self):
        """
        Returns the currently active input
        """
        url = self.url + 'menu_native/dynamic/tv_settings/devices/current_input'
        response = self.session.get(url)
        input = json.loads(response.text)
        return input
        
    def getSettings(self):
        url = self.url + 'menu_native/dynamic/tv_settings/mobile_devices'
        response = self.session.get(url)
        return response.text

    
    def powerOn(self):
        url = self.url + 'key_command/'
        data = {
            'KEYLIST' : [
                {'CODESET' : 11, 'CODE' : 1, 'ACTION' : 'KEYPRESS'}
            ]
        }
        response = self.session.put(url,json.dumps(data), headers={'Content-Type':'application/json'})
        return response
        
    def powerOff(self):
        url = self.url + 'key_command/'
        data = {
            'KEYLIST' : [
                {'CODESET' : 11, 'CODE' : 0, 'ACTION' : 'KEYPRESS'}
            ]
        }
        response = self.session.put(url,json.dumps(data), headers={'Content-Type':'application/json'})
        return response