import config
import connector
import handler

def main():
    central_config, room_configs = config.get_configs()
    
    distributedServerConnector = connector.DistributedServerConnector()

    distributedServerConnector.register_readable_handler(handler.handler_func)

    for room in room_configs:
        address = connector.Address(room['ip_servidor_distribuido'], room['porta_servidor_distribuido'])
        distributedServerConnector.connect(address)

    distributedServerConnector.serve()

if __name__ == "__main__":
    main()