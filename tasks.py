import time
from celery import Celery

BROKER_URL = "redis://:redispassword@cache:6379/0"
app = Celery(
    'tasks',
    broker=BROKER_URL,
    worker_prefetch_multiplier=1,
)

# https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html#redis-caveats
app.conf.broker_transport_options = {'visibility_timeout': 5}
app.conf.result_backend_transport_options = {'visibility_timeout': 5}
app.conf.visibility_timeout = 5


@app.task
def example(timeout):
    print(f"Timeout: {timeout}")
    time.sleep(timeout)
    print(f"Finished: {timeout}.")
    print()

if __name__ == '__main__':
    args = ['worker', '-c10', '--loglevel=INFO']
    app.worker_main(argv=args)
