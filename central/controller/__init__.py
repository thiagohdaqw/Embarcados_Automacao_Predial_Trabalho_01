from . import buildings, router, http, rooms

def init(app: router.HttpRouter):
    app.register_route(router.HttpMethod.GET, '/api/buildings', buildings.get_building)

    app.register_route(router.HttpMethod.POST, '/api/buildings/alarm-system', buildings.toogle_alarm_system)
    app.register_route(router.HttpMethod.POST, '/api/buildings/lamps', buildings.update_lamps)
    app.register_route(router.HttpMethod.POST, '/api/buildings/relays', buildings.update_relays)

    app.register_route(router.HttpMethod.POST, '/api/rooms/relays', rooms.toggle_relay)