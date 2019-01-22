from flask_restplus import fields
from rest_api_oscar.api.restplus import api

status = api.model('Status', {
    "id": fields.String(readOnly=True,description="id of the status, as String value"),
    "declaredStatusName": fields.String(required=True,description="Status set by Member"),
    "calculatedStatusName": fields.String(readOnly=True, description="Status set by WDQMS"),
    "memberSince":  fields.Date(required=True,description="date since")
})

program = api.model('Program', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a a program'),
    "program" : fields.String(required=True,description="program/network"),
    "approvalStatus" : fields.String(description="Approval Status"),
    "programSpecificId" : fields.String(description="Approval Status"),
    "programUrl" : fields.String(description="Approval Status"),    
    "stationProgramStatuses" : fields.List( fields.Nested(status) )
})

territory = api.model('Territory', {
    "validSince": fields.Date(required=True, description="since when"),
    "territoryName": fields.String(required=True, description="name of territory"),
})

timezone = api.model('Time-Zone', {
    "validSince": fields.Date(required=True, description="since when"),
    "timezoneName": fields.String(required=True, description="name of territory"),
})

location = api.model('Location', {
    "validSince": fields.Date(required=True, description="since when"),
    "latitude": fields.String(required=True, description="latitude"),
    "longitude": fields.String(required=True, description="longitude"),
    "elevation": fields.Integer(required=True, description="elevation"),
    "geoposName": fields.String( description="internal field"),
})

wigosid = api.model('WIGOS identifier' ,{
    'id': fields.Integer(readOnly=True, description='The unique identifier of a wigosid'),
    'wid': fields.String(required=True, description="Station description"),
    'primary' : fields.Boolean(description="WIGOS identifier")
})

description = api.model('Station description' ,{
    'id': fields.Integer(readOnly=True, description='The unique identifier of a description'),
    'validSince': fields.Date(required=True,description='validity date of description'),
    'description': fields.String(required=True, description="Station description"),
})

url = api.model('URL',{
    'id' : fields.Integer(readOnly=True, description='The unique identifier of a URL'),
    'dataUrl' : fields.String(required=True,description="The URL")
})


instrument_status = api.model('InstrumentStatus', {
    "statusName": fields.String(readOnly=True,description="the status, as String value"),
    "sinceDate": fields.Date(required=True,description="Date from"),
    "tillDate": fields.Date(description="Date to"),
    "memberSince":  fields.Date(required=True,description="date since")
})

instrument_catalogue = api.model('InstrumentCatalogue',{
    "model" : fields.String(description="model of instrument"),
    "manufacturer" : fields.String(description="Manufacturer")    
})


instrument = api.model('Instrument',{
    "id" : fields.Integer(readOnly=True, description='The unique identifier of the instrument'),
    "sharedInstrument" : fields.Boolean(description="is the instrument shared with other deployments"),
    "serialNumber" : fields.String(description="Serial Number"),
    "instrumentCatalogue" : fields.Nested(instrument_catalogue),
    "instrumentStatuses" : fields.List( fields.Nested(instrument_status) )
})

processing = api.model('Processing',{
    "id" : fields.Integer(readOnly=True, description='The unique identifier of a processing'),
    "aggregationInterval" : fields.Integer(description="interval of aggragation in seconds"),
    "processingMethod":  fields.String(  description="processing method" ),  
    "processorVersion":  fields.String(  description="version of software doing the processing" ),  
    "sourceCodeRepositoryUrl":  fields.String(  description="URL for data" ),  
    "organizationName":  fields.String(  description="Name of the organization doing the processing" )
})

sampling = api.model('Sampling', {
    'id' : fields.Integer(readOnly=True, description='The unique identifier of a sampling'),
	"samplingStrategyName":  fields.String(  description="Name of Sampling Strategy" ),
	"temporalSamplingInterval":  fields.Integer(  description="sampling interval" ),
	"temporalSamplingIntervalUnitName":  fields.Integer(  description="Unit of Sampling Interval" ),
	"samplingTimePeriod":  fields.String(  description="period of sampling" ),  
    "samplingTimePeriodUnitName":  fields.String(  description="Unit of sampling time period" ),  
    "spatialSamplingResolution":  fields.String(  description="Spatial sampling resolution" ),  
    "samplingProcedureName":  fields.Boolean(  description="name of sampling procedure" ),
    "samplingProcedureText":  fields.Boolean(  description="text of sampling procedure" ),
    "sampleTreatmentName":  fields.Boolean(  description="name of sampling treatments" )
} )

reporting = api.model('Reporting', {
    'id' : fields.Integer(readOnly=True, description='The unique identifier of a reporting'),
	"dataLevelName":  fields.String(  description="month from" ),
	"dataPolicyName":  fields.String(  description="month from" ),
	"temporalReportingInterval":  fields.Integer( attribute='temporalReportingIntervalDB' , description="reporting interval in seconds" ),
	"variableUnitName":  fields.String(  description="name of variable unit" ),  
	"isInternationalExchange":  fields.Boolean(  description="is the data shared internationally" ),  
	"dataFormatName":  fields.String(  description="name of data format" ),  
	"referenceTimeSourceName":  fields.String(  description="name of reference time source name" ),  
    "qualityFlagSystemName":  fields.String(  description="name of quality system flag" ),  
    "traceabilityName":  fields.String(  description="name of tracability" ),  
    "aggregationIntervalTimestampName":  fields.String(  description="nameof aggregation time interval" ),  
} )

schedule = api.model('Schedule',{
    "id": fields.Integer(readOnly=True, description='The unique identifier of the data generation'),
	"monthSinceName":  fields.String( required=True, description="month from" ),
    "monthTillName": fields.String( required=True, description="month to" ),
    "weekdaySinceName":  fields.String( required=True, description="day from" ),
    "weekdayTillName": fields.String( required=True, description="day to" ),
    "hourSince" : fields.Integer( required=True , description="hour from"),
    "hourTo" : fields.Integer( required=True , description="hour to"),
    "minuteSince" : fields.Integer( required=True , description="minute from"),
    "minuteTill" : fields.Integer( required=True , description="minute to"),
    "diurnalBaseHour": fields.Integer( required=True , description="diurnal hour"),
    "diurnalBaseMinute": fields.Integer( required=True , description="diurnal minute")
})

data_generation = api.model('DataGeneration',{
    "id": fields.Integer(readOnly=True, description='The unique identifier of the data generation'),
	"dataSubmittedFrom":  fields.Date( required=True, description="date from" ),
    "dataSubmittedTo": fields.Date( required=True, description="date to" ),
    "observationSince":  fields.Date( required=True, description="date from" ),
    "observationTill": fields.Date( required=True, description="date to" ),
    "schedule" : fields.Nested(schedule),
    "reporting" : fields.Nested(reporting),
    "sampling" : fields.Nested(sampling),
    "processing" : fields.Nested(processing)
})

deployment = api.model('Observation', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a description'),
    'lastModifiedBy' : fields.String(readOnly=True,description="last modified by"),
    'sourceName' : fields.String(required=True,description="The source of the observation"),
    'distanceFromRefSurface' : fields.Integer(description="The distance of the deployed instrument from the surface"),
    'typeOfReferenceSurfaceName' : fields.String(description="type of reference surface"),
    'dataUrls' : fields.List(fields.Nested(url)),
    'deplSince' : fields.Date(required=True,description="Date since"),
    'deplTill' : fields.Date(required=True,description="Date to"),
    'nrt' : fields.Boolean(description="near real time data available"),
    'dataCenterName' : fields.String(description="name of data center"),
    'observationName' : fields.String(readOnly=True,description="summary description"),
    'measurementLeaderName' : fields.String(description="Measurement leader"),
    'representativenessName' : fields.String(description="Measurement leader"),
    'dataCommunicationMethodName' : fields.String(description="Measurement leader"),
    'organizationName' : fields.String(description="name of organization "),
    'exposureName' : fields.String(description="name of exposure"),
    'dataGenerations' : fields.List( fields.Nested(data_generation) )
})

observation = api.model('Observation' ,{
    'id': fields.Integer(readOnly=True, description='The unique identifier of an observation'),
    'variableName': fields.String(required=True, description="variable name"),
    'geometryName': fields.String(required=True, description="geometry name"),
    'lastModifiedOn' : fields.Date(description="last modification date/time"),
    'programs' : fields.List(fields.Nested(program)),
    'deployments' : fields.List(fields.Nested(deployment)),
    
})

station = api.model('Oscar Station', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a station'),
    'name': fields.String(required=True, description='Station name'),
    'wmoRaName': fields.String(required=True, description='WMO Region'),
    'typeName': fields.String(required=True, description='Station type'),
    'typeName': fields.String(required=True, description='Station type'),
    'dateEstablished': fields.Date,
    'observations': fields.List(fields.Nested(observation),required=True),    
    'descriptions': fields.List(fields.Nested(description)),
    'locations' : fields.List(fields.Nested(location),required=True),
    'timezones' : fields.List(fields.Nested(timezone),required=True),
    'territories' : fields.List(fields.Nested(territory),required=True),
    'wigosIds' : fields.List(fields.Nested(wigosid),required=True),
    'stationPrograms' : fields.List(fields.Nested(program),required=True)
})

station_search = api.model('Oscar Station in search', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a station'),
    'name': fields.String(required=True, description='Station name'),
    'wmoIndex': fields.String(required=True, description='Station identifier'),
    'region': fields.String(required=True, description='WMO region'),
    'territory': fields.String(required=True, description='WMO Member'),
    'longitude': fields.Float(required=True, description='Longitude of station'),
    'latitude': fields.Float(required=True, description='Latitude of station'),
    'elevation': fields.Integer(required=True, description='Latitude of station'),
    'stationTypeName': fields.String(required=True, description='Station type'),
    'stationTypeId': fields.Integer(required=True, description='Station type id'),
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})


