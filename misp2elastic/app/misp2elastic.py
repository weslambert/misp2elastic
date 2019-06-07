import time
import yaml
import requests
import requests
from pymisp import PyMISP
from config import parser
from pymemcache.client.base import Client
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

memcached_host = parser.get('memcached', 'host')
memcached_port = int(parser.get('memcached', 'port'))
memcached_agetime = int(parser.get('memcached', 'agetime'))
memcached_sleeptime = int(parser.get('memcached', 'sleeptime'))
memcached = Client((memcached_host, memcached_port))
misp_url = parser.get('misp', 'url')
misp_key = parser.get('misp', 'apikey')
misp_verifycert = parser.getboolean('misp', 'verifycert')

def getAttrs():
    def init(url,key):
      return PyMISP(url, key, misp_verifycert, 'json')
    misp = init(misp_url, misp_key)
    call_path = 'attributes/restSearch'
    with open('misp2elastic.yaml', 'r') as f:
        mispyaml = yaml.safe_load(f)
        for i in mispyaml["iocs"]:
          for t in  mispyaml["iocs"][i]["tags"]:
            search = '{"returnFormat":"json", "type":"' + i + '", "tags":"' + t + '"}'
            response = misp.direct_call(call_path, search)   
            for event in response['response']['Attribute']:
              item = event['value']
              if item != "":
                memcached_key = i + '-' + item
                try:
                  memcached.set(memcached_key, t, memcached_agetime)
                except: 
                  print("An error occurred!")
    time.sleep(memcached_sleeptime)
while True:
    getAttrs()          
