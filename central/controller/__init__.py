from ..distributed_server import consumer
from . import rooms, router, http

def init(app: router.HttpRouter):
    app.register_route(router.HttpMethod.GET, '/api/buildings', rooms.get_building)
    # web_router.register_route(HttpMethod.POST, '/api/triggers', report.get_current_report)