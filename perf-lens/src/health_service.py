class HealthService:

    def liveness(self):
        return {
            "status": "UP"
        }