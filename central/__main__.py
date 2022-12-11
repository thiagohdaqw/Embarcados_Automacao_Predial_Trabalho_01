import config
from server import Address, Server, HttpMethod
import handler
import web


def main():
    central_config, room_configs = config.get_configs()

    server = Server(
        server_address=Address(
            central_config['ip_servidor_central'],
            central_config['porta_servidor_central']
        ))

    server.register_readable_handler(handler.handler_func)
    server.register_http_handler(HttpMethod.GET, web.handle_get_method)

    for room in room_configs:
        address = Address(room['ip_servidor_distribuido'],
                          room['porta_servidor_distribuido'])
        server.connect(address)

    server.serve()


if __name__ == "__main__":
    main()
