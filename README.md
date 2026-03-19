# Incr-Upgrade-Locust


Locust load test setup for KubeRay incremental upgrade.

> A Locust test is essentially just a Python program making requests to the system you want to test.


## Experiments

- `fruit` v0
  - 1 head, 1 worker
  - 2 ProxyActors with low CPU load (~ 0 on head, ~ 30 on the worker)
  - RPS ~ 100

- `simple` v0
  - 1 head, 1 worker
  - Ray Serve autoscaling (1, 2)
  - 2 ProxyActors with low CPU load on worker (> 100 on head, < 20 on the worker)
  - Users 10 -> RPS ~ 800

- `simple` v1
  - 1 head, 1 worker (scaling up to 3)
  - Ray Serve autoscaling (1, 3)
  - 4 ProxyActors with low CPU load on worker (> 100 on head, ~ 35 on the worker)
  - Users 10 -> RPS 900+

## Problems

- Limitations on `fruit`
  - POST with price calculation?

### Test Env Setup

- CI might have the same version mismatch issue as below

```bash
The Kubernetes version v1.29.0 is not supported by Istio 1.28.3. The minimum supported Kubernetes version is 1.30.
Proceeding with the installation, but you might experience problems. See https://istio.io/latest/docs/releases/supported-releases/ for a list of supported versions.
```
