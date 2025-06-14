# from locust import HttpUser, TaskSet, task, between
# class UserBehavior(TaskSet):
#     @task
#     def login(self):
#         self.client.post("/sign_up/", {"email": "bt24ece013@iiitn.ac.in", "password": "1234"})

# class WebsiteUser(HttpUser):
#     tasks = [UserBehavior]
#     wait_time = between(1, 5)


from locust import HttpUser, task, between
import uuid

class EduGenieUser(HttpUser):
    wait_time = between(1, 3)  # wait between 1 and 3 seconds between tasks

    @task
    def signup(self):
        unique_email = f"user_{uuid.uuid4()}@example.com"
        payload = {
            "name": "Test User",
            "email": unique_email,
            "password": "TestPassword123",
            "school_student": False
        }
        headers = {"Content-Type": "application/json"}

        response = self.client.post("/sign_up/", json=payload, headers=headers)
        if response.status_code == 201:
            print(f"Successfully signed up: {unique_email}")
        else:
            print(f"Failed signup: {response.status_code} - {response.text}")
