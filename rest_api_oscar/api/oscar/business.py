#from rest_api_oscar.database.models import Station
from rest_api_oscar.oscarlib.oscar_client import OscarClient
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequest
from flask import current_app
import logging

log = logging.getLogger(__name__)

def __resolve_codelist(codelist,name,element,name_id):
    
    codelists = current_app.config["codelists"]
    if not codelist in codelists:
        raise Exception("codelist {} not known".format(codelist))

    if name in element:
        if element[name] in codelists[codelist]:
            element[name_id] = codelists[codelist][element[name]]
        else:
            raise BadRequest("{} not in codelist {}".format(element[name],codelist))
    
    
def __resolve_codelists(station):

    log.debug(station)

    __resolve_codelist("WmoRaRef","wmoRaName",station, "wmoRaId" )
    __resolve_codelist("StationTypeRef","typeName",station, "typeId" )

    for territory in station["territories"]:
        __resolve_codelist("TerritoryRef","territoryName",territory, "territoryId" )

    for timezone in station["timezones"]:
        __resolve_codelist("TimezoneRef","timezoneName",timezone, "timezoneId" )

    for location in station["locations"]:
        __resolve_codelist("GeopositionRef","geoposName",location, "geoposId" )
        
    for program in station["stationPrograms"]:
        __resolve_codelist("ProgramNetwork","program",program, "programId" )

    for observation in station["observations"]:
        __resolve_codelist("ObservationGeometryRef","geometryName",observation, "geometryId" )
        __resolve_codelist("Variable","variableName",observation, "variableId" )
      
        for program in observation["programs"]:
            __resolve_codelist("ProgramNetwork","program",program, "programId" )
    
    return station

def __prepare_new_station(station):
    
    station["submitNewStation"] = True
    station["gawChildrenPrograms"] = 0
    station["addingGawFirstTime"] = False
    
    for location in station["locations"]:
        location["usedLocations"] = None
    
    for territory in station["territories"]:
        territory["usedTerritories"] = None
        
    for program in station["stationPrograms"]:
        program["isNew"] = True
        
    for observation in station["observations"]:
        observation["usedObservations"] = None
        observation["editObservation"] = False
        observation["editable"] = True
        observation["observationIsOpen"] = True
        observation["show"] = True
        
        for program in observation["programs"]:
            program["isNew"] = True
     
    return station


def search_stations(params):
    oscar_client = OscarClient(oscarurl=current_app.config["OSCAR_URL"])
    result =  oscar_client.oscarSearch(params)
    
    return result["data"]

def get_all_stations(page,nr_stations=None):
    oscar_client = OscarClient(oscarurl=current_app.config["OSCAR_URL"])
    stations = oscar_client.oscarSearch()
    
    start_idx = (page-1)*nr_stations
    end_idx = (page-1)*nr_stations + nr_stations
    
    result = []
    for station in stations["data"][start_idx:end_idx]:
        s = oscar_client.getFullStationJson(station["id"],level='basic')
        result.append(s)
        
        if nr_stations and len(result) >= nr_stations:
            break
        
    return result
    
def get_station(id):
    oscar_client = OscarClient(oscarurl=current_app.config["OSCAR_URL"])
    station_info = oscar_client.getFullStationJson(id,level='deployments')

    if station_info:
        return station_info
        # return Station( id=station_info["id"] , name=station_info["name"], 
        # date_established = station_info["dateEstablished"] , 
        # description=station_info["descriptions"][0]["description"],
        # wigosid=station_info["wigosIds"][0]["wid"]
        #)
    else:
        raise NoResultFound("No station with id {}".format(id))


def create_station(data, cookies, qlack_token):
    
    data = __prepare_new_station(data)
    data = __resolve_codelists(data)
    
    oscar_client = OscarClient(oscarurl=current_app.config["OSCAR_URL"])
    [status_code,info] = oscar_client.createStation(data,cookies,qlack_token)

    return status_code, info
    
def update_station(station_id, data, cookies, qlack_token):
    
    oscar_client = OscarClient(oscarurl=current_app.config["OSCAR_URL"])
    ret = oscar_client.updateStation(station_id,data,cookies,qlack_token)

    if ret is None :
       raise NoResultFound("No station with id {}".format(station_id))

    return ret
    
def delete_station(station_id):
    # post = Post.query.filter(Post.id == post_id).one()
    # db.session.delete(post)
    # db.session.commit()
    pass

