# Celery issue with `visibility_timeout`

Setting `visibility_timeout` to a very low value together with `acks_late=True`
and a task that takes more time than `visibility_timeout` seems to not have
effect: Celery is not redelivering the task to another worker.


## Run

```
$ docker compose up
```

### Example run

```
$ docker compose up
Attaching to cache-1, task-trigger-1, worker-1
cache-1         | 1:C 24 Jul 2025 22:38:09.061 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
cache-1         | 1:C 24 Jul 2025 22:38:09.061 # Redis version=6.2.6, bits=64, commit=00000000, modified=0, pid=1, just started
cache-1         | 1:C 24 Jul 2025 22:38:09.061 # Configuration loaded
cache-1         | 1:M 24 Jul 2025 22:38:09.061 * Increased maximum number of open files to 10032 (it was originally set to 1024).
cache-1         | 1:M 24 Jul 2025 22:38:09.061 * monotonic clock: POSIX clock_gettime
cache-1         | 1:M 24 Jul 2025 22:38:09.062 * Running mode=standalone, port=6379.
cache-1         | 1:M 24 Jul 2025 22:38:09.062 # Server initialized
cache-1         | 1:M 24 Jul 2025 22:38:09.062 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
cache-1         | 1:M 24 Jul 2025 22:38:09.062 * Loading RDB produced by version 6.2.6
cache-1         | 1:M 24 Jul 2025 22:38:09.062 * RDB age 3 seconds
cache-1         | 1:M 24 Jul 2025 22:38:09.062 * RDB memory usage when created 1.02 Mb
cache-1         | 1:M 24 Jul 2025 22:38:09.062 # Done loading RDB, keys loaded: 3, keys expired: 0.
cache-1         | 1:M 24 Jul 2025 22:38:09.062 * DB loaded from disk: 0.000 seconds
cache-1         | 1:M 24 Jul 2025 22:38:09.062 * Ready to accept connections
worker-1        | /.venv/lib/python3.12/site-packages/celery/platforms.py:841: SecurityWarning: You're running the worker with superuser privileges: this is
worker-1        | absolutely not recommended!
worker-1        | 
worker-1        | Please specify a different user using the --uid option.
worker-1        | 
worker-1        | User information: uid=0 euid=0 gid=0 egid=0
worker-1        | 
worker-1        |   warnings.warn(SecurityWarning(ROOT_DISCOURAGED.format(
worker-1        |  
worker-1        |  -------------- celery@ee9995e1d3ee v5.5.3 (immunity)
worker-1        | --- ***** ----- 
worker-1        | -- ******* ---- Linux-6.12.39-1-lts-x86_64-with-glibc2.36 2025-07-24 22:38:09
worker-1        | - *** --- * --- 
worker-1        | - ** ---------- [config]
worker-1        | - ** ---------- .> app:         tasks:0x73918cdb2420
worker-1        | - ** ---------- .> transport:   redis://:**@cache:6379/0
worker-1        | - ** ---------- .> results:     disabled://
worker-1        | - *** --- * --- .> concurrency: 10 (prefork)
worker-1        | -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
worker-1        | --- ***** ----- 
worker-1        |  -------------- [queues]
worker-1        |                 .> celery           exchange=celery(direct) key=celery
worker-1        |                 
worker-1        | 
worker-1        | [tasks]
worker-1        |   . tasks.example
worker-1        | 
task-trigger-1 exited with code 0
worker-1        | [2025-07-24 22:38:09,458: INFO/MainProcess] Connected to redis://:**@cache:6379/0
worker-1        | [2025-07-24 22:38:09,460: INFO/MainProcess] mingle: searching for neighbors
worker-1        | [2025-07-24 22:38:10,466: INFO/MainProcess] mingle: all alone
worker-1        | [2025-07-24 22:38:10,473: INFO/MainProcess] celery@ee9995e1d3ee ready.
worker-1        | [2025-07-24 22:38:10,475: INFO/MainProcess] Task tasks.example[a071090f-2648-49ec-86cd-45bef0885973] received
worker-1        | [2025-07-24 22:38:10,476: INFO/MainProcess] Task tasks.example[041a7b1f-3d50-45fa-82eb-1b92ee342162] received
worker-1        | [2025-07-24 22:38:10,477: WARNING/ForkPoolWorker-8] Timeout: 3
worker-1        | [2025-07-24 22:38:10,477: WARNING/ForkPoolWorker-1] Timeout: 10
worker-1        | [2025-07-24 22:38:10,479: INFO/MainProcess] Task tasks.example[a3836bef-effb-4497-bc14-2ed6392c9ef1] received
worker-1        | [2025-07-24 22:38:10,481: INFO/MainProcess] Task tasks.example[bc876c5b-675c-4222-ace2-c323f0464220] received
worker-1        | [2025-07-24 22:38:10,482: WARNING/ForkPoolWorker-2] Timeout: 60
worker-1        | [2025-07-24 22:38:10,482: WARNING/ForkPoolWorker-9] Timeout: 30
worker-1        | [2025-07-24 22:38:10,482: INFO/MainProcess] Task tasks.example[adc84f45-be9a-40bc-894d-144df0e38706] received
worker-1        | [2025-07-24 22:38:10,483: WARNING/ForkPoolWorker-10] Timeout: 90


worker-1        | [2025-07-24 22:38:13,477: WARNING/ForkPoolWorker-8] Finished: 3.
worker-1        | [2025-07-24 22:38:13,478: INFO/ForkPoolWorker-8] Task tasks.example[a071090f-2648-49ec-86cd-45bef0885973] succeeded in 3.001120472999901s: None
worker-1        | [2025-07-24 22:38:15,482: ERROR/MainProcess] Task handler raised error: TimeLimitExceeded(5)
worker-1        | Traceback (most recent call last):
worker-1        |   File "/.venv/lib/python3.12/site-packages/billiard/pool.py", line 684, in on_hard_timeout
worker-1        |     raise TimeLimitExceeded(job._timeout)
worker-1        | billiard.einfo.ExceptionWithTraceback: 
worker-1        | """
worker-1        | Traceback (most recent call last):
worker-1        |   File "/.venv/lib/python3.12/site-packages/billiard/pool.py", line 684, in on_hard_timeout
worker-1        |     raise TimeLimitExceeded(job._timeout)
worker-1        | billiard.exceptions.TimeLimitExceeded: TimeLimitExceeded(5,)
worker-1        | """
worker-1        | [2025-07-24 22:38:15,482: ERROR/MainProcess] Hard time limit (5s) exceeded for tasks.example[041a7b1f-3d50-45fa-82eb-1b92ee342162]
worker-1        | [2025-07-24 22:38:15,586: ERROR/MainProcess] Process 'ForkPoolWorker-1' pid:11 exited with 'signal 9 (SIGKILL)'



worker-1        | [2025-07-24 22:38:40,482: WARNING/ForkPoolWorker-9] Finished: 30.
worker-1        | [2025-07-24 22:38:40,483: INFO/ForkPoolWorker-9] Task tasks.example[a3836bef-effb-4497-bc14-2ed6392c9ef1] succeeded in 30.00088241099911s: None
worker-1        | [2025-07-24 22:39:10,482: WARNING/ForkPoolWorker-2] Finished: 60.
worker-1        | [2025-07-24 22:39:10,483: INFO/ForkPoolWorker-2] Task tasks.example[bc876c5b-675c-4222-ace2-c323f0464220] succeeded in 60.00086987500072s: None
worker-1        | [2025-07-24 22:39:40,484: WARNING/ForkPoolWorker-10] Finished: 90.
worker-1        | [2025-07-24 22:39:40,484: INFO/ForkPoolWorker-10] Task tasks.example[adc84f45-be9a-40bc-894d-144df0e38706] succeeded in 90.00119466400065s: None
```
