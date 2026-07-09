from locust import HttpUser, task, between


class LoadTestUser(HttpUser):
    # Replace with your backend URL while running
    host = "http://localhost:8000"

    wait_time = between(1, 2)

    headers = {
        "Content-Type": "application/json"
    }

    # ------------------------
    # Health Check
    # ------------------------
    @task(2)
    def health(self):
        self.client.get("/health")

    # ------------------------
    # Login
    # ------------------------
    @task(2)
    def login(self):

        payload = {
            "email": "admin@test.com",
            "password": "admin123"
        }

        self.client.post(
            "/auth/login",
            json=payload,
            headers=self.headers
        )

    # ------------------------
    # User Profile
    # ------------------------
    @task(2)
    def profile(self):

        self.client.get(
            "/users/profile",
            headers=self.headers
        )

    # ------------------------
    # Chat Endpoint
    # ------------------------
    @task(3)
    def chat(self):

        payload = {
            "message": "Explain Machine Learning"
        }

        self.client.post(
            "/chat",
            json=payload,
            headers=self.headers
        )

    # ------------------------
    # RAG Search
    # ------------------------
    @task(2)
    def rag_search(self):

        payload = {
            "query": "What is Artificial Intelligence?"
        }

        self.client.post(
            "/rag/search",
            json=payload,
            headers=self.headers
        )

    # ------------------------
    # Documents
    # ------------------------
    @task(1)
    def documents(self):

        self.client.get(
            "/documents",
            headers=self.headers
        )