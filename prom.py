import requests
import json
import time
import logging
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server, push_to_gateway, Gauge, CollectorRegistry
from logger import custom_logging

logger = logging.getLogger(__name__)
class CustomCollector(object):
    
    def __init__(self):
        pass
        
    def collect(self):
        try :
            with open('metrics.json') as f:
                data = json.load(f)
                metrics_data = data.items()
                g = GaugeMetricFamily(
                    'instana_metrics_exporter', 'Metrics exported from instana for critical APIs', labels=['METRICS', 'API','PAGE'])
                for k, v in metrics_data:
                    if k != "Empty" :
                        API = v['label'] 
                        ERRONEOUSCALLS = v['erroneousCalls'] 
                        TOTALCALLS = v['totalCalls'] 
                        LATENCYMEAN =  v['latencyMean'] 
                        LATENCYP95 = v['latencyP95']
                        LATENCYP75 = v['latencyP75']
                        PAGE = v['page'] 
                        g.add_metric(['erroneousCalls', API,PAGE],ERRONEOUSCALLS)
                        g.add_metric(['totalcalls',API ,PAGE],TOTALCALLS)
                        g.add_metric(['latencymean',API,PAGE],LATENCYMEAN)
                        g.add_metric(['latencyp95',API,PAGE],LATENCYP95 )
                        g.add_metric(['latencyp75', API, PAGE], LATENCYP75)
                yield g
        except OSError as e:
            logger.error(e)

def updateMetrics() :
    '''
    Push metrics to 1080 port inorder to be picked up by prometheus
    '''
    try:
        start_http_server(1080)
        REGISTRY.register(CustomCollector())
        time.sleep(20)
    except Exception as e:
        logger.error(e)