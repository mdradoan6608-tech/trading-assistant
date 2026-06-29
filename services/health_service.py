from datetime import datetime


class HealthService:
    def __init__(self):
        self.started_at = datetime.now()

    def uptime(self):
        delta = datetime.now() - self.started_at

        seconds = int(delta.total_seconds())

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        return f"{hours}h {minutes}m {secs}s"
