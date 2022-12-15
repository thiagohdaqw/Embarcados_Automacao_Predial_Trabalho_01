from central.model.building import Building
from .http import build_json_response

def get_building(request: str, building: Building) -> bytes:
    return build_json_response(building.asdict())
