## cancal-rollback

### Result: PASS

### Locust Summary

| Metric | Value |
|--------|-------|
| Total Requests | 229,668 |
| Total Failures | 0 |
| Failure Rate | 0.00% |
| Avg Response Time | 7.8707ms |
| P99 Response Time | 25.0000ms |
| RPS | 1247.01reqs/s |

### Test Goals

- [x] active_tc monotonically increasing during rollback
- [x] active_trp monotonically increasing during rollback
- [x] pending_tc monotonically decreasing during rollback
- [x] pending_trp monotonically decreasing during rollback
- [x] Zero Locust failures

### Timeline

| Elapsed | Phase | Active TC | Active TRP | Pending TC | Pending TRP | Upgrading | Rolling Back |
|---------|-------|-----------|------------|------------|-------------|-----------|--------------|
|     0.2 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|     2.2 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|     4.3 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|     6.3 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|     8.4 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    10.4 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    12.5 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    14.5 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    16.6 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    18.6 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    20.7 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    22.8 | wait_for_rs_ready |       100 |        100 |          - |           - |     False |        False |
|    23.9 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    25.1 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    26.1 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    27.1 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    28.2 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    29.2 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    30.3 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    31.4 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    32.4 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    33.5 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    34.5 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    35.6 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    36.6 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    37.7 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    38.7 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    39.8 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    40.8 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    41.9 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    43.0 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    44.0 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    45.1 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    46.1 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    47.2 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    48.2 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    49.3 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    50.3 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    51.4 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    52.4 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    52.6 | upgrading    |       100 |        100 |          - |           - |      True |        False |
|    53.7 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    54.8 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    55.9 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    56.9 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    58.0 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    59.1 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    60.1 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    61.2 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    62.2 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    63.3 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    64.4 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    65.4 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    66.5 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    67.5 | upgrading    |       100 |        100 |         20 |           0 |      True |        False |
|    68.6 | upgrading    |       100 |        100 |         20 |           0 |      True |        False |
|    69.7 | upgrading    |       100 |        100 |         20 |           0 |      True |        False |
|    70.7 | upgrading    |       100 |        100 |         20 |           0 |      True |        False |
|    71.8 | upgrading    |       100 |        100 |         20 |           0 |      True |        False |
|    72.9 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|    73.9 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|    75.0 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|    76.0 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|    77.1 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|    78.2 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|    79.2 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|    80.3 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|    81.3 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|    82.4 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|    83.5 | upgrading    |       100 |         80 |         20 |          20 |      True |        False |
|    84.5 | upgrading    |       100 |         80 |         20 |          20 |      True |        False |
|    85.6 | upgrading    |        80 |         80 |         20 |          20 |      True |        False |
|    86.6 | upgrading    |        80 |         80 |         20 |          20 |      True |        False |
|    87.7 | upgrading    |        80 |         80 |         40 |          20 |      True |        False |
|    88.8 | upgrading    |        80 |         80 |         40 |          20 |      True |        False |
|    89.8 | upgrading    |        80 |         80 |         40 |          20 |      True |        False |
|    90.8 | upgrading    |        80 |         80 |         40 |          20 |      True |        False |
|    91.9 | upgrading    |        80 |         80 |         40 |          20 |      True |        False |
|    93.0 | upgrading    |        80 |         80 |         40 |          20 |      True |        False |
|    94.0 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|    95.1 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|    96.2 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|    97.2 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|    98.3 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|    99.3 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   100.4 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   101.5 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   102.5 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   103.6 | upgrading    |        80 |         60 |         40 |          40 |      True |        False |
|   103.8 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   104.8 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   105.9 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   107.0 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   108.0 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   109.1 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   110.1 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   111.2 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   112.3 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   113.3 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   114.4 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   115.5 | rolling_back |        80 |         70 |         40 |          30 |      True |         True |
|   116.5 | rolling_back |        80 |         70 |         40 |          30 |      True |         True |
|   117.6 | rolling_back |        80 |         70 |         40 |          30 |      True |         True |
|   118.6 | rolling_back |        80 |         70 |         40 |          30 |      True |         True |
|   119.7 | rolling_back |        80 |         70 |         40 |          30 |      True |         True |
|   120.8 | rolling_back |        80 |         70 |         40 |          30 |      True |         True |
|   121.8 | rolling_back |        80 |         70 |         40 |          30 |      True |         True |
|   122.9 | rolling_back |        80 |         70 |         40 |          30 |      True |         True |
|   123.9 | rolling_back |        80 |         70 |         40 |          30 |      True |         True |
|   125.0 | rolling_back |        80 |         80 |         40 |          20 |      True |         True |
|   125.2 | canceling_rollback |        80 |         80 |         40 |          20 |      True |        False |
|   126.3 | canceling_rollback |        80 |         80 |         40 |          20 |      True |        False |
|   127.3 | canceling_rollback |        80 |         80 |         40 |          20 |      True |        False |
|   128.4 | canceling_rollback |        80 |         80 |         40 |          20 |      True |        False |
|   129.4 | canceling_rollback |        80 |         80 |         40 |          20 |      True |        False |
|   130.5 | canceling_rollback |        80 |         80 |         40 |          20 |      True |        False |
|   131.6 | canceling_rollback |        80 |         80 |         40 |          20 |      True |        False |
|   132.6 | canceling_rollback |        80 |         80 |         40 |          20 |      True |        False |
|   133.7 | canceling_rollback |        80 |         80 |         40 |          20 |      True |        False |
|   134.7 | canceling_rollback |        80 |         80 |         40 |          20 |      True |        False |
|   135.8 | canceling_rollback |        80 |         70 |         40 |          30 |      True |        False |
|   136.8 | canceling_rollback |        80 |         70 |         40 |          30 |      True |        False |
|   137.9 | canceling_rollback |        80 |         70 |         40 |          30 |      True |        False |
|   138.9 | canceling_rollback |        80 |         70 |         40 |          30 |      True |        False |
|   140.0 | canceling_rollback |        80 |         70 |         40 |          30 |      True |        False |
|   141.1 | canceling_rollback |        80 |         70 |         40 |          30 |      True |        False |
|   142.1 | canceling_rollback |        80 |         70 |         40 |          30 |      True |        False |
|   143.2 | canceling_rollback |        80 |         70 |         40 |          30 |      True |        False |
|   144.2 | canceling_rollback |        80 |         70 |         40 |          30 |      True |        False |
|   145.3 | canceling_rollback |        80 |         60 |         40 |          40 |      True |        False |
|   146.3 | canceling_rollback |        80 |         60 |         40 |          40 |      True |        False |
|   147.4 | canceling_rollback |        60 |         60 |         40 |          40 |      True |        False |
|   148.5 | canceling_rollback |        60 |         60 |         60 |          40 |      True |        False |
|   149.5 | canceling_rollback |        60 |         60 |         60 |          40 |      True |        False |
|   150.6 | canceling_rollback |        60 |         60 |         60 |          40 |      True |        False |
|   151.6 | canceling_rollback |        60 |         60 |         60 |          40 |      True |        False |
|   152.7 | canceling_rollback |        60 |         60 |         60 |          40 |      True |        False |
|   153.7 | canceling_rollback |        60 |         60 |         60 |          40 |      True |        False |
|   154.8 | canceling_rollback |        60 |         60 |         60 |          40 |      True |        False |
|   155.8 | canceling_rollback |        60 |         50 |         60 |          50 |      True |        False |
|   156.9 | canceling_rollback |        60 |         50 |         60 |          50 |      True |        False |
|   158.0 | canceling_rollback |        60 |         50 |         60 |          50 |      True |        False |
|   159.1 | canceling_rollback |        60 |         50 |         60 |          50 |      True |        False |
|   160.1 | canceling_rollback |        60 |         50 |         60 |          50 |      True |        False |
|   161.2 | canceling_rollback |        60 |         50 |         60 |          50 |      True |        False |
|   162.2 | canceling_rollback |        60 |         50 |         60 |          50 |      True |        False |
|   163.3 | canceling_rollback |        60 |         50 |         60 |          50 |      True |        False |
|   164.3 | canceling_rollback |        60 |         50 |         60 |          50 |      True |        False |
|   165.4 | canceling_rollback |        60 |         50 |         60 |          50 |      True |        False |
|   166.4 | canceling_rollback |        60 |         40 |         60 |          60 |      True |        False |
|   167.5 | canceling_rollback |        60 |         40 |         60 |          60 |      True |        False |
|   168.6 | canceling_rollback |        40 |         40 |         60 |          60 |      True |        False |
|   169.6 | canceling_rollback |        40 |         40 |         60 |          60 |      True |        False |
|   170.7 | canceling_rollback |        40 |         40 |         80 |          60 |      True |        False |
|   171.7 | canceling_rollback |        40 |         40 |         80 |          60 |      True |        False |
|   172.8 | canceling_rollback |        40 |         40 |         80 |          60 |      True |        False |
|   173.8 | canceling_rollback |        40 |         40 |         80 |          60 |      True |        False |
|   174.9 | canceling_rollback |        40 |         40 |         80 |          60 |      True |        False |
|   175.9 | canceling_rollback |        40 |         40 |         80 |          60 |      True |        False |
|   177.0 | canceling_rollback |        40 |         30 |         80 |          70 |      True |        False |
|   178.1 | canceling_rollback |        40 |         30 |         80 |          70 |      True |        False |
|   179.1 | canceling_rollback |        40 |         30 |         80 |          70 |      True |        False |
|   180.2 | canceling_rollback |        40 |         30 |         80 |          70 |      True |        False |
|   181.3 | canceling_rollback |        40 |         30 |         80 |          70 |      True |        False |
|   182.3 | canceling_rollback |        40 |         30 |         80 |          70 |      True |        False |
|   183.4 | canceling_rollback |        40 |         30 |         80 |          70 |      True |        False |
|   184.4 | canceling_rollback |        40 |         30 |         80 |          70 |      True |        False |
|   185.5 | canceling_rollback |        40 |         30 |         80 |          70 |      True |        False |
|   186.6 | canceling_rollback |        40 |         20 |         80 |          80 |      True |        False |
|   187.6 | canceling_rollback |        40 |         20 |         80 |          80 |      True |        False |
|   188.7 | canceling_rollback |        20 |         20 |         80 |          80 |      True |        False |
|   189.7 | canceling_rollback |        20 |         20 |         80 |          80 |      True |        False |
|   190.8 | canceling_rollback |        20 |         20 |        100 |          80 |      True |        False |
|   191.8 | canceling_rollback |        20 |         20 |        100 |          80 |      True |        False |
|   192.9 | canceling_rollback |        20 |         20 |        100 |          80 |      True |        False |
|   193.9 | canceling_rollback |        20 |         20 |        100 |          80 |      True |        False |
|   195.0 | canceling_rollback |        20 |         20 |        100 |          80 |      True |        False |
|   196.1 | canceling_rollback |        20 |         20 |        100 |          80 |      True |        False |
|   197.1 | canceling_rollback |        20 |         10 |        100 |          90 |      True |        False |
|   198.2 | canceling_rollback |        20 |         10 |        100 |          90 |      True |        False |
|   199.2 | canceling_rollback |        20 |         10 |        100 |          90 |      True |        False |
|   200.3 | canceling_rollback |        20 |         10 |        100 |          90 |      True |        False |
|   201.3 | canceling_rollback |        20 |         10 |        100 |          90 |      True |        False |
|   202.4 | canceling_rollback |        20 |         10 |        100 |          90 |      True |        False |
|   203.4 | canceling_rollback |        20 |         10 |        100 |          90 |      True |        False |
|   204.5 | canceling_rollback |        20 |         10 |        100 |          90 |      True |        False |
|   205.6 | canceling_rollback |        20 |         10 |        100 |          90 |      True |        False |
|   206.6 | canceling_rollback |        20 |         10 |        100 |          90 |      True |        False |
|   207.7 | canceling_rollback |        20 |          0 |        100 |         100 |      True |        False |
|   208.7 | canceling_rollback |       100 |        100 |          - |           - |     False |        False |
|   208.7 | complete     |       100 |        100 |          - |           - |     False |        False |
