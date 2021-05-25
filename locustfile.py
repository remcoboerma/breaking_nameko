from locust import HttpUser, task, between, tag, constant
import random


class SamenhangendeComponentenTest(HttpUser):
    wait_time = constant(1)

    @tag("simple")
    @task(1)
    def simple(self):
        # _from = 1 if random.randint(1, 100) < 60 else random.randint(1, 80)
        self.client.get("/simple")

    @tag("sleepy")
    @task(1)
    def met_sleep(self):
        # _from = 1 if random.randint(1, 100) < 60 else random.randint(1, 80)
        self.client.get("/sleep/10")

    # @tag("simple_request")
    # @task()
    # def met_simple_requests(self):
    #     # _from = 1 if random.randint(1, 100) < 60 else random.randint(1, 80)
    #     self.client.get("/request?url=http://graphql/simple")
    #
    # @tag("sleepy_request")
    # @task()
    # def met_sleepy_requests(self):
    #     # _from = 1 if random.randint(1, 100) < 60 else random.randint(1, 80)
    #     self.client.get("/request?url=http://graphql/sleep/10")
