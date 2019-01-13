import json, base64 
import requests, csv, logging

OSCAR_TOKEN = "X-OSCAR-api-token"
CODES_URL = "http://test.wmocodes.info"

log = logging.getLogger(__name__)

def __read_program_codelist_rec(entry,ret):
    ret[entry["text"]] = entry["id"]
    
    if 'children' in entry:
        for child_entry in entry["children"]:
            __read_program_codelist_rec(child_entry,ret)

def __read_program_codelist(codelist):
    ret = {}
    for entry in codelist:
        __read_program_codelist_rec(entry,ret)
        
    return ret

def read_reference_codelist(url):
    
    ret = { None : None , "null" : None }
    
    with requests.Session() as s:
        log.info("loading reference cocdelist: {}".format(url))
        r = s.get(url)
        
        codelist = json.loads( r.content )
        
        if "program-tree" in url or "variableTree" in url : # programnetwork affiliation and variable have different codelist
            return __read_program_codelist(codelist)

        for row in codelist:
            ret[row["name"]]=row["id"]

    return ret        
            
def decode_token(token):   
    tmp = json.loads( base64.b64decode( token )  )
    return [ tmp["cookies"] , tmp["token"] ]

def encode_token(session_info):
    return base64.b64encode( json.dumps(session_info).encode()  ).decode()

    
def read_codelist(name):
    
    if name == 'stationClass' :
        return ["aerodrome","agrimetStation","coastalStation","helideckOffshore","hurricaneForecastCentre","seaplaneBase",
                "lightship","lighthouse","mountainStation","riverForecastCentre","tidalWaveForecastCentre","upperWindNAVAID",
                "windProfiler","upperWindRadar","upperWindRadioTheodolite","upperWindComposite","radiosondeSation","weatherRadar" ]
        
    name = name.replace('wmo','WMO')
    name = "{}{}".format( name[0].capitalize() , name[1:])

    url = CODES_URL + "/wmdr/{type}?_format=csv".format(type=name)

    ret = []
    with requests.Session() as s:
        log.info("loading cocdelist: {}".format(url))
        download = s.get(url)
        
        decoded_content = download.content.decode('utf-8')
        cr = csv.DictReader(decoded_content.splitlines(), delimiter=',' ,  )
        for row in cr:
            ret.append(row["skos:notation"])

    return ret