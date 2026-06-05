from shapely.geometry import Point

def find_district(lat: float, lng: float, districts: list) -> int | None:
    point = Point(lng, lat)
    for district_id, polygon in districts:
        if polygon.covers(point):
            return district_id
    return None