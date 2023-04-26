from fastapi import FastAPI, APIRouter ,Depends
from sqlalchemy.orm import Session
from data.connection import get_db
from data import models
from data import schema
from geopy.point import Point
import math
router = APIRouter()

@router.get("/all")
def get_all_address_list(db: Session = Depends(get_db)):
    return db.query(models.Address).all()

@router.get("/{address_id}")
def get_address(address_id: int,db: Session = Depends(get_db)):
    return db.query(models.Address).filter(models.Address.id == address_id).first()

def check_validity_coordinates(latitude,longitude):
    try:
        Point(latitude, longitude)
        return True
    except ValueError:
        return False

@router.post("/add",status_code=200)
def add_address(request: schema.AddressAdd,db: Session = Depends(get_db)):
    try:
        latitude = request.latitude
        longitude = request.longitude
        if check_validity_coordinates(latitude,longitude):
            address = models.Address(name=request.name, latitude=latitude,
                              longitude=longitude,
                              active=True)
            db.add(address)
            db.commit()
            return "Address Added"

        else:
            return "Not Valid Address"

    except:
        return "Not Valid Address"


@router.post("/update/{address_id}",status_code=200)
def update_address(address_id: int,request: schema.AddressAdd,db: Session = Depends(get_db)):
    address = db.query(models.Address).filter(models.Address.id == address_id)
    if address.first():
        try:
            latitude = request.latitude
            longitude = request.longitude
            if check_validity_coordinates(latitude,longitude):
                address.update({
                    "name": request.name,
                    "latitude": request.latitude,
                    "longitude": request.longitude
                })
                db.commit()
                return "Address Update"

            else:
                return "Not Valid Address"

        except:
            return "Not Valid Address"
    else:
        return "Address not exist"

@router.delete("/{address_id}")
def delete_address(address_id: int,db: Session = Depends(get_db)):
    doc = db.query(models.Address).filter(models.Address.id == address_id).first()
    db.delete(doc)
    db.commit()
    return {"detail": "delete"}

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

@router.post("/distance/{address_id}",status_code=200)
def get_address_in_a_distance(request: schema.CalculateDistance,db: Session = Depends(get_db)):
    addresses = db.query(models.Address).all()
    filtered_addresses = []
    for address in addresses:
        distance = haversine_distance(request.latitude,request.longitude, address.latitude, address.longitude)
        if distance <= request.distance:
            filtered_addresses.append(address)
    return filtered_addresses





