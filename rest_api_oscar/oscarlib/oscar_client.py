import requests
import json
import datetime
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse
import logging

WIGOSID_SEARCH_URL = '//rest/api/stations/approvedStations/wigosIds?q={wigosid}'
STATION_SEARCH_URL = '//rest/api/search/station?stationClass={stationClass}'
STATION_DETAILS_URL = '//rest/api/stations/station/{internal_id}/stationReport'
STATION_OSERVATIONS_GROUPING_URL = '//rest/api/stations/observation/grouping/{internal_id}'
DEPLOYMENT_URL = '//rest/api/stations/deployments/{observation_id}'

OSCAR_SEARCH_URL = '//rest/api/search/station'

logging.basicConfig(level=logging.INFO)

class OscarClient(object):

    def __init__(self,**kwargs):
        self.oscar_url = kwargs.get('oscarurl')

    def oscarSearch(params):
       oscar_search_url = self.oscar_url + OSCAR_SEARCH_URL
       rsp = requests.get( oscar_search_url , params=params )
       
       if rsp.status_code == 200:
          myjson={}
          myjson["data"] = json.loads(  rsp.content )
          myjson["meta"] = { 'length' : len(myjson["data"]) }
       else:
          ret = {}
          ret["status_code"] = rsp.status_code
          ret["message"] = str(rsp.content) 
          #myjson = json.dumps(  ret  )
       return myjson 

       
    def getInternalIDfromWigosId(self,wigosid):
        wigosid_search_url = self.oscar_url + WIGOSID_SEARCH_URL
        rsp=requests.get( wigosid_search_url.format(wigosid=wigosid) )
        stations = json.loads(rsp.content)
        internal_id = stations[0]["id"]
        return internal_id
        

        
    def getFullStationJson(self,internal_id, **kwargs ):
        
        filterObs = False
        if 'observations' in kwargs:
            filterObs = True
            validObservations = kwargs['observations']
            logging.debug("limiting observations to {}".format(validObservations))

        station_details_url = self.oscar_url + STATION_DETAILS_URL
        logging.debug("getting station details for {} from {}".format(internal_id,station_details_url))
        rsp=requests.get( station_details_url.format(internal_id=internal_id) )
        
        if not rsp.status_code == 200:
            logging.debug("station {} not found".format(internal_id))
            return None
            
        station_info = json.loads(rsp.content)

        if not 'basicOnly' in kwargs:
            logging.info("getting station observation groups for {}".format(internal_id))
            station_observations_grouping_url = self.oscar_url +  STATION_OSERVATIONS_GROUPING_URL
            rsp=requests.get( station_observations_grouping_url.format(internal_id=internal_id) )
            observation_groups = json.loads(rsp.content)

            observations = []

            # iterate over observations and retrieve schedules
            for observationgroup in observation_groups:
                for observation in observationgroup['observationTitle']:
                    observation_id = int(observation['observationId'])
                    variable_id = int(observation['observAccordionId'].split('_')[0])
                    observation['variable_id'] = variable_id
                    
                    if filterObs and not variable_id in validObservations:
                        logging.debug("filtering out observation {} since not in {}".format(variable_id,validObservations))
                        continue

                    logging.info("getting deployment {}".format(observation_id))
                    deployment_url = self.oscar_url + DEPLOYMENT_URL
                    rsp = requests.get( deployment_url.format(observation_id=observation_id))
                    deployment = json.loads(rsp.content)

                    observation['deployments'] = deployment

                    observations.append(observation)

        if not 'basicOnly' in kwargs:
            station_info['observations'] = observations
        
        if not 'dateEstablished' in station_info:
            station_info["dateEstablished"] = None
        
        return station_info


    def extractSchedulesByVariable(self,station_info, onlyActiveDeployments=True , referenceDate = datetime.datetime.today() ):
        
        result = {}
        if not 'observations' in station_info:
            return result
        
        observations = station_info['observations'] 
        
        for observation in observations:
            var_id = observation['observAccordionId'].split('_')[0]
            result[var_id] = []
            
            if not 'deployments' in observation:
                continue
            
            deployments = observation['deployments']
            
            for deployment in deployments:
                if onlyActiveDeployments:
                    datefrom = datetime.strptime(deployment['observationSince'],'%Y-%m-%d') if 'observationSince' in deployment else datetime.datetime(datetime.MINYEAR,1,1)
                    dateto =  datetime.strptime(deployment['observationTill'],'%Y-%m-%d') if 'observationTill' in deployment else datetime.datetime(datetime.MAXYEAR,1,1)

                    if not ( datefrom <= referenceDate and referenceDate <= referenceDate ):
                        logging.debug("skipping date from: {} to: {} today:".format(datefrom,dateto,referenceDate))
                        continue
                    
                if not 'dataGenerations' in deployment:
                    continue
                  
                data_generations = deployment['dataGenerations']
                
            for data_generation in data_generations:
                if not ( 'schedule' in data_generation and 'reporting' in data_generation   ) :
                   logging.debug("skipping DG due to incomplete information {}".format(data_generation))
                   continue

                schedule = data_generation['schedule']
                reporting = data_generation['reporting']
                logging.debug("adding schedule and reporting info to result")
                result[var_id].append( { 'schedule' : schedule , 'reporting': reporting } )

                    
        return result
             