import requests
import json
import time
import logging
from config import build_config
from config import build_auth
from prom import updateMetrics
from logger import custom_logging

custom_logging(logging.INFO)
logger = logging.getLogger(__name__)
def instana_exporter () :
    conf = build_config()
    auth = build_auth()
    url= auth['url']
    apitoken= auth['token']
    epochtime= int(time.time())*1000
    headers = {
        "Content-Type" : "application/json",
        "Authorization" : "apiToken " + apitoken,
    }
    
    for i in conf.keys():
        i = str(i)
        config_list = str.split(conf[i],',')
        data={
        "applicationBoundaryScope": "ALL",
        "applicationId": config_list[0],
        "endpointId": config_list[2],
        "endpointTypes": ["HTTP"],
        "excludeSynthetic": True,
        "metrics": [{
            "aggregation": "SUM",
            "metric": "calls"
        }, 
        {       
            "aggregation": "SUM",
            "metric": "erroneousCalls"   
        },
        {
            "aggregation": "MEAN",
            "metric": "latency"   
        },
        {
            "aggregation": "P95",
            "metric": "latency"   
        },
        {
            "aggregation": "P75",
            "metric": "latency"
        }
        ],
        "serviceId": config_list[1],
        "timeFrame": {
        "to": epochtime,
        "windowSize": 300000
            }       
        }            
        try : 
            Response = requests.post(url, data=json.dumps(data), headers=headers)
            if Response.status_code == 200:
                instana_response = Response.json()
                page = int(i)-1
                metrics_json=parse_json(instana_response,page)
                with open('metrics.json') as json_file:
                    data = json.load(json_file)
                    data.update(metrics_json)
                with open("metrics.json", "w") as Count_metrics:
                    json.dump(data, Count_metrics, indent=4) 
            else :
                logger.error('Bad response from Instana')   
        except requests.exceptions.RequestException as e : 
            logger.error(e)


def parse_json(instana_response, page):
    metrics={}
    empty = []
    conf = build_config()
    page_list = []
    for i in conf.keys() : 
        i = str(i)
        config_list = str.split(conf[i],',')
        page_list.append(config_list[3])
    try:
        if 'items' in instana_response and len(instana_response['items'])>0 : 
            label=instana_response['items'][0]['endpoint']['label']
            metrics["label"] = instana_response['items'][0]['endpoint']['label']
            metrics["erroneousCalls"] = instana_response['items'][0]['metrics']['erroneousCalls.sum'][0][1]
            metrics["totalCalls"] = instana_response['items'][0]['metrics']['calls.sum'][0][1]
            metrics["latencyMean"] = instana_response['items'][0]['metrics']['latency.mean'][0][1]
            metrics["latencyP95"] = instana_response['items'][0]['metrics']['latency.p95'][0][1]
            metrics["latencyP75"] = instana_response['items'][0]['metrics']['latency.p75'][0][1]
            metrics["page"] = page_list[page]
            api_metrics[label]=metrics
            return api_metrics  
        else :
            label="Empty"
            empty = {"Response" : "Recieved Empty response"}
            api_metrics[label]=empty
            return api_metrics
    except Exception as e :
        logger.error(e)  
        

if __name__ == '__main__':
    api_metrics = {}
    try :
        while True:
            instana_exporter()
            updateMetrics()
            logger.info("Code Executed")
            time.sleep(310) #adding 10 second grace period, allowing prometheus to end method
    except Exception as e :
        logger.error(e)