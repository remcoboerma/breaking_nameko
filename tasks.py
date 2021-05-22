import sys
import webbrowser

from invoke import task
from plumbum import BG
from plumbum.cmd import nameko, locust

import time


@task()
def run(ctx, web=True):
    # nameko service to run
    nameko_service = nameko["run", "services:Service"]
    # locust test runner for simple request. should work near instantly
    locust_simple = locust[
        "--tags", "simple", "--host", "http://localhost:8000", "-P", 8081
    ]
    # if headless
    if not web:
        locust_simple = locust_simple[
            "--headless",
            "--users",
            100,
            "--spawn-rate",
            50,
            "--run-time",
            55,
            "--only-summary",
        ]
    locust_sleepy = locust[
        "--tags", "sleepy", "--host", "http://localhost:8000", "-P", 8080
    ]
    if not web:
        locust_sleepy = locust_sleepy[
            "--headless",
            "--users",
            60,
            "--spawn-rate",
            60,
            "--run-time",
            60,
            "--only-summary",
        ]

    if web:
        with nameko_service.bgrun(
            stdout=sys.stdout, stderr=sys.stderr
        ) as nameko_instance:
            time.sleep(2)
            with locust_simple.bgrun() as simple_job:
                time.sleep(5)
                locust_sleepy & BG
            time.sleep(1)
            nameko_instance.terminate()

        time.sleep(1)
        webbrowser.open_new_tab("http://localhost:8080")
        webbrowser.open_new_tab("http://localhost:8081")
    else:
        # headless
        with nameko_service.bgrun(
            stdout=sys.stdout, stderr=sys.stderr
        ) as nameko_instance:
            time.sleep(1)
            with locust_simple.bgrun(stdout=sys.stdout) as simple_job:
                time.sleep(5)
                locust_sleepy & BG(stdout=sys.stdout)
            time.sleep(1)
            nameko_instance.terminate()
