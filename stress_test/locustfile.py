from locust import HttpUser, between, task

class UserBehavior(HttpUser):
    wait_time = between(0.5, 1)

    @task(1)
    def index(self):
        self.client.get("http://localhost/")

    @task(3)
    def predict(self):
        files = [
            ("file", ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg"))
        ]
        headers = {}
        payload = {}
        self.client.post(
            "http://localhost/predict",
            headers = headers,
            data = payload,
            files = files,
        )
