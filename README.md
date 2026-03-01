# Incr-Upgrade-Locust


Locust load test setup for KubeRay incremental upgrade.

> A Locust test is essentially just a Python program making requests to the system you want to test.


## Experiments

- `fruit` v0: 1 head, 1 worker
  - RPS ~ 100
  - 2 ProxyActors with low CPU load (~ 0 on head, ~ 30 on the worker)
