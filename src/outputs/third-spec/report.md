## third-spec

### Result: PASS

### Locust Summary

| Metric | Value |
|--------|-------|
| Total Requests | 295,622 |
| Total Failures | 0 |
| Failure Rate | 0.00% |
| Avg Response Time | 8.3464ms |
| P99 Response Time | 46.0000ms |
| RPS | 1176.52reqs/s |

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
|    12.4 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    14.5 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    16.6 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    18.6 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    20.7 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    22.7 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    24.8 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    26.8 | wait_for_rs_ready |           |            |        100 |           - |     False |        False |
|    28.9 | wait_for_rs_ready |       100 |        100 |          - |           - |     False |        False |
|    30.0 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    31.1 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    32.1 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    33.2 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    34.2 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    35.3 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    36.3 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    37.4 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    38.4 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    39.5 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    40.5 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    41.6 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    42.6 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    43.7 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    44.8 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    45.8 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    46.9 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    47.9 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    49.0 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    50.0 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    51.1 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    52.1 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    53.2 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    54.2 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    55.3 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    56.4 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    57.4 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    58.5 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    59.5 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    60.6 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    61.6 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    62.7 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    63.8 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    64.8 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    65.9 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    66.9 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    68.0 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    69.0 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    70.1 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    71.2 | locust_warmup |       100 |        100 |          - |           - |     False |        False |
|    71.4 | upgrading    |       100 |        100 |          - |           - |      True |        False |
|    72.4 | upgrading    |       100 |        100 |          - |           - |      True |        False |
|    73.5 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    74.6 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    75.7 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    76.7 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    77.8 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    78.8 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    79.9 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    81.0 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    82.0 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    83.1 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    84.1 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    85.2 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|    86.3 | upgrading    |       100 |        100 |         20 |           0 |      True |        False |
|    87.3 | upgrading    |       100 |        100 |         20 |           0 |      True |        False |
|    88.4 | upgrading    |       100 |        100 |         20 |           0 |      True |        False |
|    89.4 | upgrading    |       100 |        100 |         20 |           0 |      True |        False |
|    90.5 | upgrading    |       100 |        100 |         20 |           0 |      True |        False |
|    91.6 | upgrading    |       100 |        100 |         20 |           0 |      True |        False |
|    92.6 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|    93.7 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|    94.7 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|    95.8 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|    96.9 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|    97.9 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|    99.0 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|   100.0 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|   101.1 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|   102.1 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|   103.2 | upgrading    |       100 |         80 |         20 |          20 |      True |        False |
|   104.3 | upgrading    |       100 |         80 |         20 |          20 |      True |        False |
|   105.3 | upgrading    |        80 |         80 |         20 |          20 |      True |        False |
|   106.4 | upgrading    |        80 |         80 |         20 |          20 |      True |        False |
|   107.5 | upgrading    |        80 |         80 |         40 |          20 |      True |        False |
|   108.5 | upgrading    |        80 |         80 |         40 |          20 |      True |        False |
|   109.6 | upgrading    |        80 |         80 |         40 |          20 |      True |        False |
|   110.6 | upgrading    |        80 |         80 |         40 |          20 |      True |        False |
|   111.7 | upgrading    |        80 |         80 |         40 |          20 |      True |        False |
|   112.7 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   113.8 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   114.8 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   115.9 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   117.0 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   118.0 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   119.1 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   120.1 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   121.2 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   122.2 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   123.3 | upgrading    |        80 |         60 |         40 |          40 |      True |        False |
|   123.5 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   124.6 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   125.6 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   126.7 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   127.8 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   128.8 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   129.9 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   130.9 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   132.0 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   133.1 | rolling_back |        80 |         60 |         40 |          40 |      True |         True |
|   134.1 | rolling_back |        80 |         70 |         40 |          30 |      True |         True |
|   135.2 | rolling_back |        80 |         70 |         40 |          30 |      True |         True |
|   136.3 | rolling_back |        80 |         70 |         40 |          30 |      True |         True |
|   137.3 | rolling_back |        80 |         70 |         40 |          30 |      True |         True |
|   138.4 | rolling_back |        80 |         70 |         40 |          30 |      True |         True |
|   139.4 | rolling_back |        80 |         70 |         40 |          30 |      True |         True |
|   140.5 | rolling_back |        80 |         70 |         40 |          30 |      True |         True |
|   141.6 | rolling_back |        80 |         70 |         40 |          30 |      True |         True |
|   142.6 | rolling_back |        80 |         70 |         40 |          30 |      True |         True |
|   143.7 | rolling_back |        80 |         80 |         40 |          20 |      True |         True |
|   143.9 | upgrading    |        80 |         80 |         40 |          20 |      True |         True |
|   145.0 | upgrading    |       100 |         80 |         20 |          20 |      True |         True |
|   146.0 | upgrading    |       100 |         80 |         20 |          20 |      True |         True |
|   147.1 | upgrading    |       100 |         80 |         20 |          20 |      True |         True |
|   148.2 | upgrading    |       100 |         80 |         20 |          20 |      True |         True |
|   149.2 | upgrading    |       100 |         80 |         20 |          20 |      True |         True |
|   150.3 | upgrading    |       100 |         80 |         20 |          20 |      True |         True |
|   151.3 | upgrading    |       100 |         80 |         20 |          20 |      True |         True |
|   152.4 | upgrading    |       100 |         80 |         20 |          20 |      True |         True |
|   153.4 | upgrading    |       100 |         80 |         20 |          20 |      True |         True |
|   154.5 | upgrading    |       100 |         90 |         20 |          10 |      True |         True |
|   155.6 | upgrading    |       100 |         90 |         20 |          10 |      True |         True |
|   156.6 | upgrading    |       100 |         90 |         20 |          10 |      True |         True |
|   157.7 | upgrading    |       100 |         90 |         20 |          10 |      True |         True |
|   158.7 | upgrading    |       100 |         90 |         20 |          10 |      True |         True |
|   159.8 | upgrading    |       100 |         90 |         20 |          10 |      True |         True |
|   160.8 | upgrading    |       100 |         90 |         20 |          10 |      True |         True |
|   161.9 | upgrading    |       100 |         90 |         20 |          10 |      True |         True |
|   163.0 | upgrading    |       100 |         90 |         20 |          10 |      True |         True |
|   164.0 | upgrading    |       100 |        100 |         20 |           0 |      True |         True |
|   165.1 | upgrading    |       100 |        100 |         20 |           0 |      True |         True |
|   166.1 | upgrading    |       100 |        100 |          - |           - |      True |        False |
|   167.2 | upgrading    |       100 |        100 |          - |           - |      True |        False |
|   168.2 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|   169.3 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|   170.4 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|   171.4 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|   172.5 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|   173.6 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|   174.6 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|   175.7 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|   176.8 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|   177.8 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|   178.9 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|   179.9 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|   181.0 | upgrading    |       100 |        100 |          0 |           0 |      True |        False |
|   182.1 | upgrading    |       100 |        100 |         20 |           0 |      True |        False |
|   183.1 | upgrading    |       100 |        100 |         20 |           0 |      True |        False |
|   184.2 | upgrading    |       100 |        100 |         20 |           0 |      True |        False |
|   185.2 | upgrading    |       100 |        100 |         20 |           0 |      True |        False |
|   186.3 | upgrading    |       100 |        100 |         20 |           0 |      True |        False |
|   187.4 | upgrading    |       100 |        100 |         20 |           0 |      True |        False |
|   188.4 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|   189.5 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|   190.6 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|   191.6 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|   192.7 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|   193.7 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|   194.8 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|   195.8 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|   196.9 | upgrading    |       100 |         90 |         20 |          10 |      True |        False |
|   197.9 | upgrading    |       100 |         80 |         20 |          20 |      True |        False |
|   199.0 | upgrading    |       100 |         80 |         20 |          20 |      True |        False |
|   200.1 | upgrading    |        80 |         80 |         20 |          20 |      True |        False |
|   201.1 | upgrading    |        80 |         80 |         20 |          20 |      True |        False |
|   202.2 | upgrading    |        80 |         80 |         40 |          20 |      True |        False |
|   203.2 | upgrading    |        80 |         80 |         40 |          20 |      True |        False |
|   204.3 | upgrading    |        80 |         80 |         40 |          20 |      True |        False |
|   205.3 | upgrading    |        80 |         80 |         40 |          20 |      True |        False |
|   206.4 | upgrading    |        80 |         80 |         40 |          20 |      True |        False |
|   207.4 | upgrading    |        80 |         80 |         40 |          20 |      True |        False |
|   208.5 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   209.6 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   210.6 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   211.7 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   212.7 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   213.8 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   214.8 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   215.9 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   216.9 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   218.0 | upgrading    |        80 |         70 |         40 |          30 |      True |        False |
|   219.1 | upgrading    |        80 |         60 |         40 |          40 |      True |        False |
|   220.1 | upgrading    |        80 |         60 |         40 |          40 |      True |        False |
|   221.2 | upgrading    |        60 |         60 |         40 |          40 |      True |        False |
|   222.2 | upgrading    |        60 |         60 |         40 |          40 |      True |        False |
|   223.3 | upgrading    |        60 |         60 |         60 |          40 |      True |        False |
|   224.3 | upgrading    |        60 |         60 |         60 |          40 |      True |        False |
|   225.4 | upgrading    |        60 |         60 |         60 |          40 |      True |        False |
|   226.4 | upgrading    |        60 |         60 |         60 |          40 |      True |        False |
|   227.5 | upgrading    |        60 |         60 |         60 |          40 |      True |        False |
|   228.6 | upgrading    |        60 |         60 |         60 |          40 |      True |        False |
|   229.6 | upgrading    |        60 |         50 |         60 |          50 |      True |        False |
|   230.7 | upgrading    |        60 |         50 |         60 |          50 |      True |        False |
|   231.7 | upgrading    |        60 |         50 |         60 |          50 |      True |        False |
|   232.8 | upgrading    |        60 |         50 |         60 |          50 |      True |        False |
|   233.8 | upgrading    |        60 |         50 |         60 |          50 |      True |        False |
|   234.9 | upgrading    |        60 |         50 |         60 |          50 |      True |        False |
|   235.9 | upgrading    |        60 |         50 |         60 |          50 |      True |        False |
|   237.0 | upgrading    |        60 |         50 |         60 |          50 |      True |        False |
|   238.1 | upgrading    |        60 |         50 |         60 |          50 |      True |        False |
|   239.1 | upgrading    |        60 |         40 |         60 |          60 |      True |        False |
|   240.2 | upgrading    |        60 |         40 |         60 |          60 |      True |        False |
|   241.2 | upgrading    |        40 |         40 |         60 |          60 |      True |        False |
|   242.3 | upgrading    |        40 |         40 |         60 |          60 |      True |        False |
|   243.3 | upgrading    |        40 |         40 |         80 |          60 |      True |        False |
|   244.4 | upgrading    |        40 |         40 |         80 |          60 |      True |        False |
|   245.4 | upgrading    |        40 |         40 |         80 |          60 |      True |        False |
|   246.5 | upgrading    |        40 |         40 |         80 |          60 |      True |        False |
|   247.5 | upgrading    |        40 |         40 |         80 |          60 |      True |        False |
|   248.6 | upgrading    |        40 |         40 |         80 |          60 |      True |        False |
|   249.6 | upgrading    |        40 |         30 |         80 |          70 |      True |        False |
|   250.7 | upgrading    |        40 |         30 |         80 |          70 |      True |        False |
|   251.7 | upgrading    |        40 |         30 |         80 |          70 |      True |        False |
|   252.8 | upgrading    |        40 |         30 |         80 |          70 |      True |        False |
|   253.8 | upgrading    |        40 |         30 |         80 |          70 |      True |        False |
|   254.9 | upgrading    |        40 |         30 |         80 |          70 |      True |        False |
|   255.9 | upgrading    |        40 |         30 |         80 |          70 |      True |        False |
|   257.0 | upgrading    |        40 |         30 |         80 |          70 |      True |        False |
|   258.1 | upgrading    |        40 |         30 |         80 |          70 |      True |        False |
|   259.1 | upgrading    |        40 |         30 |         80 |          70 |      True |        False |
|   260.2 | upgrading    |        40 |         20 |         80 |          80 |      True |        False |
|   261.2 | upgrading    |        40 |         20 |         80 |          80 |      True |        False |
|   262.3 | upgrading    |        20 |         20 |         80 |          80 |      True |        False |
|   263.3 | upgrading    |        20 |         20 |        100 |          80 |      True |        False |
|   264.4 | upgrading    |        20 |         20 |        100 |          80 |      True |        False |
|   265.4 | upgrading    |        20 |         20 |        100 |          80 |      True |        False |
|   266.5 | upgrading    |        20 |         20 |        100 |          80 |      True |        False |
|   267.5 | upgrading    |        20 |         20 |        100 |          80 |      True |        False |
|   268.6 | upgrading    |        20 |         20 |        100 |          80 |      True |        False |
|   269.6 | upgrading    |        20 |         10 |        100 |          90 |      True |        False |
|   270.7 | upgrading    |        20 |         10 |        100 |          90 |      True |        False |
|   271.8 | upgrading    |        20 |         10 |        100 |          90 |      True |        False |
|   272.8 | upgrading    |        20 |         10 |        100 |          90 |      True |        False |
|   273.9 | upgrading    |        20 |         10 |        100 |          90 |      True |        False |
|   274.9 | upgrading    |        20 |         10 |        100 |          90 |      True |        False |
|   276.0 | upgrading    |        20 |         10 |        100 |          90 |      True |        False |
|   277.0 | upgrading    |        20 |         10 |        100 |          90 |      True |        False |
|   278.1 | upgrading    |        20 |         10 |        100 |          90 |      True |        False |
|   279.1 | upgrading    |        20 |         10 |        100 |          90 |      True |        False |
|   280.2 | upgrading    |        20 |          0 |        100 |         100 |      True |        False |
|   281.2 | upgrading    |        20 |          0 |        100 |         100 |      True |        False |
|   282.3 | upgrading    |       100 |        100 |          - |           - |     False |        False |
|   282.3 | complete     |       100 |        100 |          - |           - |     False |        False |
