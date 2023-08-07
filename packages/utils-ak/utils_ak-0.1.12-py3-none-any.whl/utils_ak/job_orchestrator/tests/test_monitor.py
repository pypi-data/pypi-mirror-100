import time
import multiprocessing


from utils_ak.loguru import configure_loguru_stdout
from utils_ak.simple_microservice import run_listener_async
from utils_ak.job_orchestrator.worker.test.test_worker import TestWorker
from utils_ak.job_orchestrator.monitor import Monitor

from utils_ak.job_orchestrator.config import settings

MESSAGE_BROKER = settings.as_dict()["TRANSPORT"]["message_broker"]


def run_monitor():
    configure_loguru_stdout("DEBUG")
    monitor = Monitor(MESSAGE_BROKER)
    monitor.microservice.run()


def run_worker():
    configure_loguru_stdout("DEBUG")
    worker = TestWorker(
        "WorkerId",
        {"type": "batch", "message_broker": MESSAGE_BROKER},
    )
    worker.run()


def test():
    configure_loguru_stdout("DEBUG")
    run_listener_async("monitor_out", message_broker=MESSAGE_BROKER)
    time.sleep(1)

    multiprocessing.Process(target=run_monitor).start()
    time.sleep(3)
    multiprocessing.Process(target=run_worker).start()


if __name__ == "__main__":
    test()
