import time
from tasks import example


# This task should finish successfully
example.apply_async(
    args=(3,),
    acks_late=True,
    time_limit=5,
)

# This task should hit time limit and finish unsuccessfully
example.apply_async(
    args=(10,),
    acks_late=True,
    time_limit=5,
)


# The following tasks should be re-scheduled because it takes longer than
# `visibility_timeout` and we have `acks_late=True`. However, **I suspect** that
# Celery/Kombu is not respecting this `visibility_timeout` manual configuration
# and always using the default value: 60 minutes.
# The result is these tasks run completely and finish without issues
# --I'm not expecting that, tho. I'm expecting them to be re-scheduled.
example.apply_async(
    args=(30,),
    acks_late=True,
)

example.apply_async(
    args=(60,),
    acks_late=True,
)

example.apply_async(
    args=(90,),
    acks_late=True,
)


# Triggering a task longer than 60 minutes, will hit the `visibility_timeout`
# default value and it will be re-scheduled.
example.apply_async(
    args=(4500,),  # 1h15m
    acks_late=True,
)
