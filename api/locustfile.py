from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)
    @task
    def index_page(self):
        self.client.get("/")

    @task
    def page(self):
        eventname = "your_event_name_here"  # Replace with the actual event name
        headers = {"Content-Type": "application/json"}
        payload = [{"phone": "1234567890"}, {"phone": "9876543210"}]  # Replace with actual phone numbers

        self.client.post(f"/page/{eventname}", json=payload, headers=headers)

# requests to 2 routes are made, one for paging and one for verification, paging wont work currently because database is not set up