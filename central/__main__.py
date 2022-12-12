import sys
import central.controller as controller
from .util import config
from .server.server import Address, Server
import central.handler as handler

sys.path.append('.')

def main():
    central_config = config.get_config()

    server = Server(
        server_central=Address(
            central_config['ip_servidor_central'],
            central_config['porta_servidor_central'],
        ),
        server_web=Address(
            central_config['ip_servidor_web'],
            central_config['porta_servidor_web'],
        )
    )

    web_router = controller.router.HttpRouter(server)

    controller.init(web_router)

    server.register_readable_handler(handler.handler_func)
    server.register_http_handler(web_router.handle_http_message)

    server.serve()


if __name__ == "__main__":
    main()
