from utils.logger import logger


class ServiceManager:
    def __init__(self):
        self.services = {}

    def register(self, name, service):
        self.services[name] = service
        logger.info(f"Registered service: {name}")

    def start(self):
        logger.info("Starting Trading Assistant services...")

        for name, service in self.services.items():
            logger.info(f"Starting {name}...")

            if hasattr(service, "start"):
                service.start()

        logger.info("All services started.")
