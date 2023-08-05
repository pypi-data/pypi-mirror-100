import requests
import json
def get_district_and_coords_by_address(address):
    try:
        r = requests.get(f'https://nominatim.openstreetmap.org/?addressdetails=1&q={address}&format=json&limit=1&exclude_place_ids=716498%2C144330873%2C147285032')
        r = json.loads(r.text)
        if r:
            try:
                distrct = r[0]['address']['city_district']
            except:
                distrct = None
            try:
                lat, lon = float(r[0]['lat']), float(r[0]['lon'])
            except:
                lat,lon = None,None
        return distrct, [lat, lon]
    except:
        return None, [None,None]
def get_city_and_district_by_coords(lat_lon, return_all=False):
    try:
        r = requests.get(f'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat_lon[0]}&lon={lat_lon[1]}')
        js = json.loads(r.text)
        if return_all:
            return js
        else:
            return js['address']['city'],js['address']['city_district']
    except:
        return None,None
