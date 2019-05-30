import requests
import time
import yaml
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pymemcache.client.base import Client
from config import parser
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

mem_host = parser.get('memcached', 'mem_host')
mem_port = int(parser.get('memcached', 'mem_port'))
client = Client((mem_host, mem_port))
agetime = int(parser.get('memcached', 'agetime'))
sleeptime = int(parser.get('memcached', 'sleeptime'))
proto = parser.get('misp', 'misp_proto')
misp_host = parser.get('misp', 'misp_host')
apikey = parser.get('misp', 'misp_apikey')

def getAttrs():

    headers = {
            'Authorization': apikey,
            'Accept': 'application/json',
            'Content-type': 'application/json',
             }

    with open('misp2elastic.yaml', 'r') as f:
        mispyaml = yaml.safe_load(f)
        for i in mispyaml["iocs"]:
          for t in  mispyaml["iocs"][i]["tags"]:
            data = '{"returnFormat":"text", "type":"' + i + '", "tags":"' + t + '"}'
            response = requests.post(proto + '://' + misp_host + '/attributes/restSearch', headers=headers, data=data, verify=False)
            items = (response.text).splitlines()
            for item in items:
              if item != "":
                memkey = i + '-' + item
                try:
                  client.set(memkey, t, agetime)
                except: 
                  print("An error occurred!")
    time.sleep(sleeptime)

while True:
    getAttrs()          
