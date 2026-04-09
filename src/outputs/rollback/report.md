## rollback

### Result: PASS

### Locust Summary

| Metric | Value |
|--------|-------|
| Total Requests | 75,463 |
| Total Failures | 0 |
| Failure Rate | 0.00% |
| Avg Response Time | 7.9612ms |
| P99 Response Time | 20.0000ms |
| RPS | 1234.04reqs/s |

### Test Goals

- [x] active_tc monotonically increasing during rollback
- [x] active_trp monotonically increasing during rollback
- [x] pending_tc monotonically decreasing during rollback
- [x] pending_trp monotonically decreasing during rollback
- [x] Zero Locust failures

### Timeline

| Elapsed | Phase | Active TC | Active TRP | Pending TC | Pending TRP | Upgrading | Rolling Back |
|---------|-------|-----------|------------|------------|-------------|-----------|--------------|
|     0.1 | wait_for_rs_ready |           |            |          - |           - |     False |        False |
|     2.2 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|     4.2 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|     6.3 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|     8.3 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    10.4 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    12.5 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    14.5 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    16.6 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    18.6 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    20.7 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    22.8 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    24.8 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    26.9 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    28.9 | wait_for_rs_ready |       100 |        100 |          - |           - |     False |        False |
|    30.0 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    31.2 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    32.3 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    33.3 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    34.4 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    35.4 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    36.5 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    37.5 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    38.6 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    39.6 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    40.7 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    41.7 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    42.8 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    43.8 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    44.9 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    45.9 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    47.0 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    48.0 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    49.1 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    50.1 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    51.2 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    52.2 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    53.3 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    54.4 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    55.4 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    56.5 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    57.5 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    58.6 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    59.6 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    60.7 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    61.7 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    62.8 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    63.9 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    64.9 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    66.0 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    67.0 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    68.1 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    69.2 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    69.4 | upgrading    |       100 |        100 |          - |           - |      True |        False |
|    70.4 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    71.5 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    72.6 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    73.6 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    74.7 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    75.8 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    76.8 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    77.9 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    78.9 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    80.0 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    81.0 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    82.1 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    83.2 | upgrading    |       100 |        100 |         50 |           0 |      True |        False |
|    84.2 | upgrading    |       100 |        100 |         50 |           0 |      True |        False |
|    85.3 | upgrading    |       100 |        100 |         50 |           0 |      True |        False |
|    86.3 | upgrading    |       100 |        100 |         50 |           0 |      True |        False |
|    87.4 | upgrading    |       100 |        100 |         50 |           0 |      True |        False |
|    88.5 | upgrading    |       100 |        100 |         50 |           0 |      True |        False |
|    89.5 | upgrading    |       100 |        100 |         50 |           0 |      True |        False |
|    90.6 | upgrading    |       100 |        100 |         50 |           0 |      True |        False |
|    91.6 | upgrading    |       100 |         75 |         50 |          25 |      True |        False |
|    91.9 | rolling_back |       100 |         75 |         50 |          25 |      True |         True |
|    92.9 | rolling_back |       100 |         75 |         50 |          25 |      True |         True |
|    94.0 | rolling_back |       100 |         75 |         50 |          25 |      True |         True |
|    95.0 | rolling_back |       100 |         75 |         50 |          25 |      True |         True |
|    96.1 | rolling_back |       100 |         75 |         50 |          25 |      True |         True |
|    97.2 | rolling_back |       100 |         75 |         50 |          25 |      True |         True |
|    98.2 | rolling_back |       100 |         75 |         50 |          25 |      True |         True |
|    99.3 | rolling_back |       100 |         75 |         50 |          25 |      True |         True |
|   100.3 | rolling_back |       100 |         75 |         50 |          25 |      True |         True |
|   101.4 | rolling_back |       100 |        100 |         50 |           0 |      True |         True |
|   102.5 | rolling_back |       100 |        100 |         50 |           0 |      True |         True |
|   103.5 | rolling_back |       100 |        100 |          - |           - |     False |        False |
|   103.5 | complete     |       100 |        100 |          - |           - |     False |        False |
