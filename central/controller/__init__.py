from . import report, router, http

def init(app: router.HttpRouter):
    app.register_route(router.HttpMethod.GET, '/api/report', report.get_current_report)
    # web_router.register_route(HttpMethod.POST, '/api/triggers', report.get_current_report)