import time
from tasks import example


example.apply_async(
    args=(3,),
    acks_late=True,
    time_limit=5,
)

example.apply_async(
    args=(10,),
    acks_late=True,
    time_limit=5,
)

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
