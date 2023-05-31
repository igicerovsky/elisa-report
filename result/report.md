
# Automatically Generated Markdown report

This a PoC for automatic report generation...  

## Header

Date: 231705

Ientification: GN004240-033

Comment: TODO...

## Analysis Results

| Sample type   | Sample Name               |   Pre-dilution |   Reader Data [cp/ml] |   Result [cp/ml] |    CV [%] | Note                                                               |
|:--------------|:--------------------------|---------------:|----------------------:|-----------------:|----------:|:-------------------------------------------------------------------|
| control 01    | Kontrolle01               |              1 |           2.24158e+10 |      2.24158e+10 |  11.3563  | Ruduced number of sample points. Measured 4, valid 3;              |
| sample 01     | EHU04_2311_AAV9_FT1       |             10 |         nan           |    nan           | nan       | Not enough valid sample points. Required 2, available 0;           |
| sample 02     | EHU04_2311_AAV9_FT2       |             10 |         nan           |    nan           | nan       | Not enough valid sample points. Required 2, available 0;           |
| sample 03     | EHU04_2311_AAV9_FT3       |             10 |           5.50617e+07 |      5.50617e+08 | nan       | Not enough valid sample points. Required 2, available 0;           |
| sample 04     | EHU04_2311_AAV9_W1        |             10 |         nan           |    nan           | nan       | Not enough valid sample points. Required 2, available 0;           |
| sample 05     | EHU04_2311_AAV9_E2        |           1000 |           8.54313e+09 |      8.54313e+12 |   8.46792 |                                                                    |
| sample 06     | EHU04_2311_AAV9_E1+E3     |             50 |           1.31677e+11 |      6.58384e+12 |  63.3859  | CV > 0.2; Not enough valid sample points. Required 2, available 0; |
| sample 07     | EHU04_2311_AAV9_E_DIL     |           1000 |           1.12831e+10 |      1.12831e+13 |  12.2352  |                                                                    |
| sample 08     | EHU04_2311_AAV9_Reg2      |             10 |           5.04272e+09 |      5.04272e+10 |  10.4164  |                                                                    |
| sample 09     | EHU04_2311_AAV9_Reg4      |             10 |           5.96796e+08 |      5.96796e+09 | nan       | Not enough valid sample points. Required 2, available 1;           |
| sample 10     | EHU04_2311_AAV9_Reg6      |             10 |           2.20217e+08 |      2.20217e+09 | nan       | Not enough valid sample points. Required 2, available 1;           |
| sample 11     | PPO02_2307MUQ_FT          |            100 |           4.73723e+10 |      4.73723e+12 |  30.6791  | CV > 0.2; Ruduced number of sample points. Measured 4, valid 2;    |
| sample 12     | PPO02_2307AFF_FT          |             10 |         nan           |    nan           | nan       | Not enough valid sample points. Required 2, available 0;           |
| sample 13     | PPO02_2307AFF_NE          |             10 |         nan           |    nan           | nan       | Not enough valid sample points. Required 2, available 0;           |
| sample 14     | PPO02_2307AFF_ELU         |           1000 |           2.67163e+10 |      2.67163e+13 |  22.1979  | CV > 0.2; Ruduced number of sample points. Measured 4, valid 3;    |
| sample 15     | PPO02_2307SDT_F           |            200 |           3.15974e+10 |      6.31948e+12 |  18.114   | Ruduced number of sample points. Measured 4, valid 3;              |
| sample 16     | PPO02_2307POL_FT          |             10 |           8.2948e+09  |      8.2948e+10  |   7.7785  |                                                                    |
| sample 17     | PPO02_2307POL_FLT         |           1000 |           2.15592e+10 |      2.15592e+13 |  12.8379  | Ruduced number of sample points. Measured 4, valid 3;              |
| sample 18     | EDP_2313_S02_T03_CT       |             10 |           1.03451e+10 |      1.03451e+11 |   5.27912 |                                                                    |
| sample 19     | EDP_2313_S03_T03_CT       |             10 |           8.84037e+09 |      8.84037e+10 |   3.91523 |                                                                    |
| sample 20     | EHU04_2312B_UFA_UDR       |            200 |           5.47003e+09 |      1.09401e+12 |  14.048   |                                                                    |
| sample 21     | EHU04_2312B_UFA_UDR_conc. |            200 |           7.04322e+09 |      1.40864e+12 |   2.0137  |                                                                    |

## Reference Curve Fit

$\LARGE x = {d + {a - d \over {1 + ({ x \over c })^b}} }$  

!["alt text"](./img/fit.png)

Verbose fitting progress:

|   idx |     metric | note                                                                                 |
|------:|-----------:|:-------------------------------------------------------------------------------------|
|    -1 |   0.997878 |                                                                                      |
|     0 | nan        | Optimal parameters not found: Number of calls to function has reached maxfev = 1000. |
|     1 |   0.9995   | max                                                                                  |
|     2 |   0.998006 |                                                                                      |
|     3 |   0.999024 |                                                                                      |
|     4 |   0.99771  |                                                                                      |
|     5 |   0.997778 |                                                                                      |
|     6 |   0.997886 |                                                                                      |

Fit parameters

| Parameter name   |   Estimated value |       Error | Confidence interval   |
|:-----------------|------------------:|------------:|:----------------------|
| a                |       0.0246397   | 0.0369181   | [-0.0929, 0.142]      |
| b                |       0.875882    | 0.182243    | [0.296, 1.46]         |
| c                |       1.23757e+14 | 7.98525e+16 | [-2.54e+17, 2.54e+17] |
| d                |    3278.56        | 1.84718e+06 | [-5.88e+06, 5.88e+06] |

Backfit...

| Well      |   Standard Value [cp/ml] |   Concentration backfit [cp/ml] |   Optical density |   Recovery rate [%] |
|:----------|-------------------------:|--------------------------------:|------------------:|--------------------:|
| ('A', 5)  |              1.7954e+10  |                     1.79777e+10 |            1.4609 |            100.132  |
| ('A', 6)  |              8.977e+09   |                     8.06777e+09 |            0.7627 |             89.8715 |
| ('A', 7)  |              4.4885e+09  |                     4.28226e+09 |            0.4562 |             95.405  |
| ('A', 8)  |              2.24425e+09 |                     2.5087e+09  |            0.2956 |            111.783  |
| ('A', 9)  |              1.12212e+09 |                     1.11438e+09 |            0.153  |             99.3099 |
| ('A', 10) |              5.61062e+08 |                     5.19868e+08 |            0.0824 |             92.6577 |
| ('A', 11) |              2.80531e+08 |                     2.56898e+08 |            0.0465 |             91.5755 |

## Sample evaluation

### Sample: controll 'k' 1

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason                  |
|:---------|-----------:|-------------------:|----------------:|:-----------------------------|
| ('A', 1) |     1.554  |                  1 |     1.94798e+10 | Backfit 1.948e+10 > 2.805e+8 |
| ('A', 2) |     0.921  |                  2 |     2.11647e+10 |                              |
| ('A', 3) |     0.5703 |                  4 |     2.4015e+10  |                              |
| ('A', 4) |     0.3327 |                  8 |     2.50038e+10 |                              |

CV = 11.4 [%]  
mean = 2.242e+10 [cp/ml]  
valid = False  
note: Ruduced number of sample points. Measured 4, valid 3;

!["alt text"](control_01.png)

### Sample: sample 's' 1

|          |   OD_delta |   plate_layout_dil |   concentration |   mask_reason |
|:---------|-----------:|-------------------:|----------------:|--------------:|
| ('B', 1) |     0.0146 |                  1 |             nan |           nan |
| ('B', 2) |     0.0118 |                  2 |             nan |           nan |
| ('B', 3) |     0.0094 |                  4 |             nan |           nan |
| ('B', 4) |     0.0081 |                  8 |             nan |           nan |

CV = nan [%]  
mean = nan [cp/ml]  
valid = False  
note: Not enough valid sample points. Required 2, available 0;

![sample_01.png](img/sample_01.png)

### Sample: sample 's' 2

|          |   OD_delta |   plate_layout_dil |   concentration |   mask_reason |
|:---------|-----------:|-------------------:|----------------:|--------------:|
| ('C', 1) |     0.0233 |                  1 |             nan |           nan |
| ('C', 2) |     0.0211 |                  2 |             nan |           nan |
| ('C', 3) |     0.0112 |                  4 |             nan |           nan |
| ('C', 4) |     0.0091 |                  8 |             nan |           nan |

CV = nan [%]  
mean = nan [cp/ml]  
valid = False  
note: Not enough valid sample points. Required 2, available 0;

![sample_02.png](img/sample_02.png)

### Sample: sample 's' 3

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason                 |
|:---------|-----------:|-------------------:|----------------:|:----------------------------|
| ('D', 1) |     0.0336 |                  1 |     5.50617e+07 | Backfit 5.506e+7 < 2.805e+8 |
| ('D', 2) |     0.0199 |                  2 |   nan           | NaN                         |
| ('D', 3) |     0.0138 |                  4 |   nan           | NaN                         |
| ('D', 4) |     0.012  |                  8 |   nan           | NaN                         |

CV = nan [%]  
mean = 5.506e+07 [cp/ml]  
valid = False  
note: Not enough valid sample points. Required 2, available 0;

![sample_03.png](img/sample_03.png)

### Sample: sample 's' 4

|          |   OD_delta |   plate_layout_dil |   concentration |   mask_reason |
|:---------|-----------:|-------------------:|----------------:|--------------:|
| ('E', 1) |     0.0133 |                  1 |             nan |           nan |
| ('E', 2) |     0.0091 |                  2 |             nan |           nan |
| ('E', 3) |     0.007  |                  4 |             nan |           nan |
| ('E', 4) |     0.0068 |                  8 |             nan |           nan |

CV = nan [%]  
mean = nan [cp/ml]  
valid = False  
note: Not enough valid sample points. Required 2, available 0;

![sample_04.png](img/sample_04.png)

### Sample: sample 's' 5

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:---------|-----------:|-------------------:|----------------:|:--------------|
| ('F', 1) |     0.8188 |                  1 |     9.21598e+09 |               |
| ('F', 2) |     0.4518 |                  2 |     9.07893e+09 |               |
| ('F', 3) |     0.2265 |                  4 |     7.71542e+09 |               |
| ('F', 4) |     0.1402 |                  8 |     8.16219e+09 |               |

CV = 8.47 [%]  
mean = 8.543e+09 [cp/ml]  
valid = True  
![sample_05.png](img/sample_05.png)

### Sample: sample 's' 6

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason                  |
|:---------|-----------:|-------------------:|----------------:|:-----------------------------|
| ('G', 1) |     3.5014 |                  1 |     4.97835e+10 | Backfit 4.978e+10 > 2.805e+8 |
| ('G', 2) |     3.0087 |                  2 |     8.36121e+10 | Backfit 4.181e+10 > 2.805e+8 |
| ('G', 3) |     2.82   |                  4 |     1.55196e+11 | Backfit 3.880e+10 > 2.805e+8 |
| ('G', 4) |     2.2412 |                  8 |     2.38115e+11 | Backfit 2.976e+10 > 2.805e+8 |

CV = 63.4 [%]  
mean = 1.317e+11 [cp/ml]  
valid = False  
note: CV > 0.2; Not enough valid sample points. Required 2, available 0;

![sample_06.png](img/sample_06.png)

### Sample: sample 's' 7

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:---------|-----------:|-------------------:|----------------:|:--------------|
| ('H', 1) |     0.991  |                  1 |     1.15312e+10 |               |
| ('H', 2) |     0.5685 |                  2 |     1.19623e+10 |               |
| ('H', 3) |     0.3297 |                  4 |     1.2363e+10  |               |
| ('H', 4) |     0.1539 |                  8 |     9.27599e+09 |               |

CV = 12.2 [%]  
mean = 1.128e+10 [cp/ml]  
valid = True  
![sample_07.png](img/sample_07.png)

### Sample: sample 's' 8

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:---------|-----------:|-------------------:|----------------:|:--------------|
| ('B', 5) |     0.5229 |                  1 |     5.41198e+09 |               |
| ('B', 6) |     0.2986 |                  2 |     5.4673e+09  |               |
| ('B', 7) |     0.1617 |                  4 |     4.95888e+09 |               |
| ('B', 8) |     0.091  |                  8 |     4.33273e+09 |               |

CV = 10.4 [%]  
mean = 5.043e+09 [cp/ml]  
valid = True  
![sample_08.png](img/sample_08.png)

### Sample: sample 's' 9

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason                 |
|:---------|-----------:|-------------------:|----------------:|:----------------------------|
| ('C', 5) |     0.1337 |                  1 |     9.55017e+08 |                             |
| ('C', 6) |     0.0616 |                  2 |     5.55273e+08 | Backfit 2.776e+8 < 2.805e+8 |
| ('C', 7) |     0.0357 |                  4 |     2.801e+08   | Backfit 7.002e+7 < 2.805e+8 |
| ('C', 8) |     0.0209 |                  8 |   nan           | NaN                         |

CV = nan [%]  
mean = 5.968e+08 [cp/ml]  
valid = False  
note: Not enough valid sample points. Required 2, available 1;

![sample_09.png](img/sample_09.png)

### Sample: sample 's' 10

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason                 |
|:---------|-----------:|-------------------:|----------------:|:----------------------------|
| ('D', 5) |     0.0654 |                  1 |     3.10457e+08 |                             |
| ('D', 6) |     0.035  |                  2 |     1.29976e+08 | Backfit 6.499e+7 < 2.805e+8 |
| ('D', 7) |     0.0223 |                  4 |   nan           | NaN                         |
| ('D', 8) |     0.0151 |                  8 |   nan           | NaN                         |

CV = nan [%]  
mean = 2.202e+08 [cp/ml]  
valid = False  
note: Not enough valid sample points. Required 2, available 1;

![sample_10.png](img/sample_10.png)

### Sample: sample 's' 11

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason                  |
|:---------|-----------:|-------------------:|----------------:|:-----------------------------|
| ('E', 5) |     2.2784 |                  1 |     3.03358e+10 | Backfit 3.034e+10 > 2.805e+8 |
| ('E', 6) |     1.6191 |                  2 |     4.08595e+10 | Backfit 2.043e+10 > 2.805e+8 |
| ('E', 7) |     1.1646 |                  4 |     5.57033e+10 |                              |
| ('E', 8) |     0.7127 |                  8 |     6.25904e+10 |                              |

CV = 30.7 [%]  
mean = 4.737e+10 [cp/ml]  
valid = False  
note: CV > 0.2; Ruduced number of sample points. Measured 4, valid 2;

![sample_11.png](img/sample_11.png)

### Sample: sample 's' 12

|          |   OD_delta |   plate_layout_dil |   concentration |   mask_reason |
|:---------|-----------:|-------------------:|----------------:|--------------:|
| ('F', 5) |     0.0131 |                  1 |             nan |           nan |
| ('F', 6) |     0.0092 |                  2 |             nan |           nan |
| ('F', 7) |     0.0083 |                  4 |             nan |           nan |
| ('F', 8) |     0.009  |                  8 |             nan |           nan |

CV = nan [%]  
mean = nan [cp/ml]  
valid = False  
note: Not enough valid sample points. Required 2, available 0;

![sample_12.png](img/sample_12.png)

### Sample: sample 's' 13

|          |   OD_delta |   plate_layout_dil |   concentration |   mask_reason |
|:---------|-----------:|-------------------:|----------------:|--------------:|
| ('G', 5) |     0.0097 |                  1 |             nan |           nan |
| ('G', 6) |     0.0078 |                  2 |             nan |           nan |
| ('G', 7) |     0.0083 |                  4 |             nan |           nan |
| ('G', 8) |     0.0084 |                  8 |             nan |           nan |

CV = nan [%]  
mean = nan [cp/ml]  
valid = False  
note: Not enough valid sample points. Required 2, available 0;

![sample_13.png](img/sample_13.png)

### Sample: sample 's' 14

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason                  |
|:---------|-----------:|-------------------:|----------------:|:-----------------------------|
| ('H', 5) |     1.5486 |                  1 |     1.94012e+10 | Backfit 1.940e+10 > 2.805e+8 |
| ('H', 6) |     1.0657 |                  2 |     2.51094e+10 |                              |
| ('H', 7) |     0.668  |                  4 |     2.89845e+10 |                              |
| ('H', 8) |     0.4213 |                  8 |     3.33702e+10 |                              |

CV = 22.2 [%]  
mean = 2.672e+10 [cp/ml]  
valid = False  
note: CV > 0.2; Ruduced number of sample points. Measured 4, valid 3;

![sample_14.png](img/sample_14.png)

### Sample: sample 's' 15

|           |   OD_delta |   plate_layout_dil |   concentration | mask_reason                  |
|:----------|-----------:|-------------------:|----------------:|:-----------------------------|
| ('B', 9)  |     1.8693 |                  1 |     2.4131e+10  | Backfit 2.413e+10 > 2.805e+8 |
| ('B', 10) |     1.2447 |                  2 |     3.00977e+10 |                              |
| ('B', 11) |     0.8001 |                  4 |     3.58743e+10 |                              |
| ('B', 12) |     0.4515 |                  8 |     3.62866e+10 |                              |

CV = 18.1 [%]  
mean = 3.16e+10 [cp/ml]  
valid = False  
note: Ruduced number of sample points. Measured 4, valid 3;

![sample_15.png](img/sample_15.png)

### Sample: sample 's' 16

|           |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:----------|-----------:|-------------------:|----------------:|:--------------|
| ('C', 9)  |     0.7849 |                  1 |     8.76811e+09 |               |
| ('C', 10) |     0.3998 |                  2 |     7.82824e+09 |               |
| ('C', 11) |     0.254  |                  4 |     8.9267e+09  |               |
| ('C', 12) |     0.1339 |                  8 |     7.65613e+09 |               |

CV = 7.78 [%]  
mean = 8.295e+09 [cp/ml]  
valid = True  
![sample_16.png](img/sample_16.png)

### Sample: sample 's' 17

|           |   OD_delta |   plate_layout_dil |   concentration | mask_reason                  |
|:----------|-----------:|-------------------:|----------------:|:-----------------------------|
| ('D', 9)  |     1.4741 |                  1 |     1.83217e+10 | Backfit 1.832e+10 > 2.805e+8 |
| ('D', 10) |     0.8847 |                  2 |     2.01887e+10 |                              |
| ('D', 11) |     0.5683 |                  4 |     2.39145e+10 |                              |
| ('D', 12) |     0.3198 |                  8 |     2.38119e+10 |                              |

CV = 12.8 [%]  
mean = 2.156e+10 [cp/ml]  
valid = False  
note: Ruduced number of sample points. Measured 4, valid 3;

![sample_17.png](img/sample_17.png)

### Sample: sample 's' 18

|           |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:----------|-----------:|-------------------:|----------------:|:--------------|
| ('E', 9)  |     0.907  |                  1 |     1.03938e+10 |               |
| ('E', 10) |     0.5332 |                  2 |     1.10798e+10 |               |
| ('E', 11) |     0.2803 |                  4 |     1.01046e+10 |               |
| ('E', 12) |     0.1603 |                  8 |     9.80219e+09 |               |

CV = 5.28 [%]  
mean = 1.035e+10 [cp/ml]  
valid = True  
![sample_18.png](img/sample_18.png)

### Sample: sample 's' 19

|           |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:----------|-----------:|-------------------:|----------------:|:--------------|
| ('F', 9)  |     0.792  |                  1 |     8.86168e+09 |               |
| ('F', 10) |     0.4611 |                  2 |     9.30498e+09 |               |
| ('F', 11) |     0.2491 |                  4 |     8.70929e+09 |               |
| ('F', 12) |     0.1442 |                  8 |     8.48555e+09 |               |

CV = 3.92 [%]  
mean = 8.84e+09 [cp/ml]  
valid = True  
![sample_19.png](img/sample_19.png)

### Sample: sample 's' 20

|           |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:----------|-----------:|-------------------:|----------------:|:--------------|
| ('G', 9)  |     0.5592 |                  1 |     5.86448e+09 |               |
| ('G', 10) |     0.334  |                  2 |     6.28107e+09 |               |
| ('G', 11) |     0.1677 |                  4 |     5.2075e+09  |               |
| ('G', 12) |     0.0936 |                  8 |     4.52708e+09 |               |

CV = 14.0 [%]  
mean = 5.47e+09 [cp/ml]  
valid = True  
![sample_20.png](img/sample_20.png)

### Sample: sample 's' 21

|           |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:----------|-----------:|-------------------:|----------------:|:--------------|
| ('H', 9)  |     0.6562 |                  1 |     7.09455e+09 |               |
| ('H', 10) |     0.3631 |                  2 |     6.96008e+09 |               |
| ('H', 11) |     0.2077 |                  4 |     6.90055e+09 |               |
| ('H', 12) |     0.1284 |                  8 |     7.2177e+09  |               |

CV = 2.01 [%]  
mean = 7.043e+09 [cp/ml]  
valid = True  
![sample_21.png](img/sample_21.png)

