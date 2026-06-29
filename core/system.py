from core.response import success


def health(service):
    return success(
        "Trading Assistant is healthy",
        {
            "uptime": service.uptime()
        }
    )
