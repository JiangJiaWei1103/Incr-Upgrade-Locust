## rollback-with-pending-crashed

### Result: PASS

### Locust Summary

| Metric | Value |
|--------|-------|
| Total Requests | 79,930 |
| Total Failures | 10 |
| Failure Rate | 0.01% |
| Avg Response Time | 10.1263ms |
| P99 Response Time | 22.0000ms |
| RPS | 973.40reqs/s |

### Test Goals

- [x] active_tc monotonically increasing during rollback
- [x] active_trp monotonically increasing during rollback
- [x] pending_tc monotonically decreasing during rollback
- [x] pending_trp monotonically decreasing during rollback
- [ ] Zero Locust failures

### Timeline

| Elapsed | Phase | Active TC | Active TRP | Pending TC | Pending TRP | Upgrading | Rolling Back |
|---------|-------|-----------|------------|------------|-------------|-----------|--------------|
|     0.2 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|     2.3 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|     4.3 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|     6.4 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|     8.4 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    10.5 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    12.6 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    14.6 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    16.7 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    18.7 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    20.8 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    22.8 | wait_for_rs_ready |       100 |        100 |          - |           - |     False |        False |
|    23.9 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    25.0 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    26.1 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    27.1 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    28.1 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    29.2 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    30.3 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    31.3 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    32.4 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    33.4 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    34.5 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    35.5 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    36.6 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    37.6 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    38.7 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    39.7 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    40.8 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    41.9 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    42.9 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    44.0 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    45.0 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    46.1 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    47.1 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    48.2 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    49.2 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    50.3 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    51.4 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    52.4 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    53.5 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    54.5 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    55.6 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    56.6 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    57.7 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    58.8 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    59.8 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    60.9 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    61.9 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    63.0 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    64.0 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    65.1 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    65.3 | upgrading    |       100 |        100 |          - |           - |      True |        False |
|    66.3 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    67.4 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    68.5 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    69.6 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    70.6 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    71.7 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    72.8 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    73.8 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    74.9 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    75.9 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    77.0 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    78.1 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    79.1 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    80.2 | upgrading    |       100 |        100 |         50 |           0 |      True |        False |
|    81.2 | upgrading    |       100 |        100 |         50 |           0 |      True |        False |
|    82.3 | upgrading    |       100 |        100 |         50 |           0 |      True |        False |
|    83.4 | upgrading    |       100 |        100 |         50 |           0 |      True |        False |
|    84.4 | upgrading    |       100 |        100 |         50 |           0 |      True |        False |
|    85.5 | upgrading    |       100 |        100 |         50 |           0 |      True |        False |
|    86.5 | upgrading    |       100 |        100 |         50 |           0 |      True |        False |
|    87.6 | upgrading    |       100 |         75 |         50 |          25 |      True |        False |
|    87.8 | rolling_back |       100 |         75 |         50 |          25 |      True |         True |
|    88.9 | rolling_back |       100 |         75 |         50 |          25 |      True |         True |
|    89.9 | rolling_back |       100 |         75 |         50 |          25 |      True |         True |
|    91.0 | rolling_back |       100 |         75 |         50 |          25 |      True |         True |
|    92.1 | rolling_back |       100 |         75 |         50 |          25 |      True |         True |
|    93.1 | rolling_back |       100 |         75 |         50 |          25 |      True |         True |
|    94.2 | rolling_back |       100 |         75 |         50 |          25 |      True |         True |
|    95.2 | rolling_back |       100 |         75 |         50 |          25 |      True |         True |
|    96.3 | rolling_back |       100 |         75 |         50 |          25 |      True |         True |
|    97.4 | rolling_back |       100 |         75 |         50 |          25 |      True |         True |
|    98.4 | rolling_back |       100 |        100 |         50 |           0 |      True |         True |
|   107.2 | rolling_back |       100 |        100 |          - |           - |     False |        False |
|   107.2 | complete     |       100 |        100 |          - |           - |     False |        False |
