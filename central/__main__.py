import central.controller as controller
from .util import config, logger
from .server.server import Server
from .server.socket import Address

def main():
    logger.init()
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

    server.register_readable_handler(controller.distributed_server.handle_distributed_server_message)
    server.register_http_handler(web_router.handle_http_message)

    server.serve()


if __name__ == "__main__":
    main()
