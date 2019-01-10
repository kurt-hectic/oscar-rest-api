#from rest_api_demo.database import db

from rest_api_oscar.database.models import Station
from rest_api_oscar.lib.oscarapi import getFullStationJson, getInternalIDfromWigosId
from sqlalchemy.orm.exc import NoResultFound

def get_all_stations():
    pass
    
def get_station(id):
    
    station_info = getFullStationJson(id,basicOnly=True)

    if station_info:
        return Station( id=station_info["id"] , name=station_info["name"], date_established = station_info["dateEstablished"] )
    else:
        raise NoResultFound("No station with id {}".format(id))


def create_station(data):
    # title = data.get('title')
    # body = data.get('body')
    # category_id = data.get('category_id')
    # category = Category.query.filter(Category.id == category_id).one()
    # post = Post(title, body, category)
    # db.session.add(post)
    # db.session.commit()
    pass

def update_station(station_id, data):
    # post = Post.query.fil ter(Post.id == post_id).one()
    # post.title = data.get('title')
    # post.body = data.get('body')
    # category_id = data.get('category_id')
    # post.category = Category.query.filter(Category.id == category_id).one()
    # db.session.add(post)
    # db.session.commit()
    pass

def delete_station(station_id):
    # post = Post.query.filter(Post.id == post_id).one()
    # db.session.delete(post)
    # db.session.commit()
    pass

