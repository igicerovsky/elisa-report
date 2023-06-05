
# Automatically Generated Markdown report

This a PoC for automatic report generation...  

## Header

Date: 231705

Ientification: GN004240-033

Comment: TODO...

## Analysis Results

| Sample type   | Sample Name               |   Pre-dilution |   Reader Data [cp/ml] |   Result [cp/ml] |    CV [%] | Valid   | Note                                                                                                                 |
|:--------------|:--------------------------|---------------:|----------------------:|-----------------:|----------:|:--------|:---------------------------------------------------------------------------------------------------------------------|
| control 01    | Kontrolle01               |              1 |           2.29252e+10 |      2.29252e+10 |  10.2274  | True    | Ruduced number of sample points. Measured 4, valid 3;>1.795e+10;Measured OD 1.554e+0 > 4.650e-2                      |
| sample 01     | EHU04_2311_AAV9_FT1       |             10 |         nan           |    nan           | nan       | False   | Not enough valid sample points. Required 2, available 0;Backfit failed.;Measured OD 1.460e-2 < 4.650e-2              |
| sample 02     | EHU04_2311_AAV9_FT2       |             10 |         nan           |    nan           | nan       | False   | Not enough valid sample points. Required 2, available 0;Backfit failed.;Measured OD 2.330e-2 < 4.650e-2              |
| sample 03     | EHU04_2311_AAV9_FT3       |             10 |           7.34788e+07 |      7.34788e+08 | nan       | False   | Not enough valid sample points. Required 2, available 0;<2.805e+8, Backfit failed., Backfit failed., Backfit failed. |
| sample 04     | EHU04_2311_AAV9_W1        |             10 |         nan           |    nan           | nan       | False   | Not enough valid sample points. Required 2, available 0;Backfit failed.;Measured OD 1.330e-2 < 4.650e-2              |
| sample 05     | EHU04_2311_AAV9_E2        |           1000 |           8.97328e+09 |      8.97328e+12 |   6.15688 | True    |                                                                                                                      |
| sample 06     | EHU04_2311_AAV9_E1+E3     |             50 |           1.2864e+11  |      6.432e+12   | nan       | False   | Not enough valid sample points. Required 2, available 0;>1.795e+10;Measured OD 3.501e+0 > 4.650e-2                   |
| sample 07     | EHU04_2311_AAV9_E_DIL     |           1000 |           1.1744e+10  |      1.1744e+13  |  10.6297  | True    |                                                                                                                      |
| sample 08     | EHU04_2311_AAV9_Reg2      |             10 |           5.38854e+09 |      5.38854e+10 |   7.37204 | True    |                                                                                                                      |
| sample 09     | EHU04_2311_AAV9_Reg4      |             10 |           6.82575e+08 |      6.82575e+09 |  33.6933  | False   | CV > 0.2; Ruduced number of sample points. Measured 4, valid 2;<2.805e+8, Backfit failed.                            |
| sample 10     | EHU04_2311_AAV9_Reg6      |             10 |           2.63199e+08 |      2.63199e+09 | nan       | False   | Not enough valid sample points. Required 2, available 1;<2.805e+8, Backfit failed., Backfit failed.                  |
| sample 11     | PPO02_2307MUQ_FT          |            100 |           4.75226e+10 |      4.75226e+12 |   9.41579 | True    | Ruduced number of sample points. Measured 4, valid 2;>1.795e+10;Measured OD 2.278e+0 > 4.650e-2                      |
| sample 12     | PPO02_2307AFF_FT          |             10 |         nan           |    nan           | nan       | False   | Not enough valid sample points. Required 2, available 0;Backfit failed.;Measured OD 1.310e-2 < 4.650e-2              |
| sample 13     | PPO02_2307AFF_NE          |             10 |         nan           |    nan           | nan       | False   | Not enough valid sample points. Required 2, available 0;Backfit failed.;Measured OD 9.700e-3 < 4.650e-2              |
| sample 14     | PPO02_2307AFF_ELU         |           1000 |           2.72252e+10 |      2.72252e+13 |  15.7959  | True    | Ruduced number of sample points. Measured 4, valid 3;>1.795e+10;Measured OD 1.549e+0 > 4.650e-2                      |
| sample 15     | PPO02_2307SDT_F           |            200 |           3.20173e+10 |      6.40346e+12 |  11.614   | True    | Ruduced number of sample points. Measured 4, valid 3;>1.795e+10;Measured OD 1.869e+0 > 4.650e-2                      |
| sample 16     | PPO02_2307POL_FT          |             10 |           8.72621e+09 |      8.72621e+10 |   6.75521 | True    |                                                                                                                      |
| sample 17     | PPO02_2307POL_FLT         |           1000 |           2.20776e+10 |      2.20776e+13 |  10.8211  | True    | Ruduced number of sample points. Measured 4, valid 3;>1.795e+10;Measured OD 1.474e+0 > 4.650e-2                      |
| sample 18     | EDP_2313_S02_T03_CT       |             10 |           1.08066e+10 |      1.08066e+11 |   3.84804 | True    |                                                                                                                      |
| sample 19     | EDP_2313_S03_T03_CT       |             10 |           9.28302e+09 |      9.28302e+10 |   2.84121 | True    |                                                                                                                      |
| sample 20     | EHU04_2312B_UFA_UDR       |            200 |           5.82542e+09 |      1.16508e+12 |  11.1533  | True    |                                                                                                                      |
| sample 21     | EHU04_2312B_UFA_UDR_conc. |            200 |           7.45562e+09 |      1.49112e+12 |   4.05828 | True    |                                                                                                                      |

## Reference Curve Fit

$\LARGE x = {d + {a - d \over {1 + ({ x \over c })^b}} }$  

!["alt text"](./img/fit.png)

Verbose fitting progress, metric is R-squared:

|   idx |     metric | note                                                                                 |
|------:|-----------:|:-------------------------------------------------------------------------------------|
|    -1 |   0.997878 | metric < threshold (0.9979 < 0.9980)                                                 |
|     0 | nan        | Optimal parameters not found: Number of calls to function has reached maxfev = 1000. |
|     1 |   0.9995   | Invalid covariance matrix.                                                           |
|     2 |   0.998006 |                                                                                      |
|     3 |   0.999024 | Maximum.                                                                             |
|     4 |   0.99771  |                                                                                      |
|     5 |   0.997778 |                                                                                      |
|     6 |   0.997886 |                                                                                      |

Fit parameters

| Parameter name   |   Estimated value |       Error | Confidence interval   |
|:-----------------|------------------:|------------:|:----------------------|
| a                |       0.0235075   | 0.0319678   | [-0.114, 0.161]       |
| b                |       0.900978    | 0.257484    | [-0.207, 2.01]        |
| c                |       9.59295e+13 | 6.83918e+16 | [-2.94e+17, 2.94e+17] |
| d                |    3267.36        | 2.09074e+06 | [-8.99e+06, 9e+06]    |

Backfit...

| Well      |   Standard Value [cp/ml] |   Concentration backfit [cp/ml] |   Optical density |   Recovery rate [%] |
|:----------|-------------------------:|--------------------------------:|------------------:|--------------------:|
| ('A', 5)  |              1.7954e+10  |                     1.80567e+10 |            1.4609 |            100.572  |
| ('A', 6)  |              8.977e+09   |                     8.62928e+09 |            0.7627 |             96.1266 |
| ('A', 7)  |              4.4885e+09  |                     4.76201e+09 |            0.4562 |            106.093  |
| ('A', 8)  |              2.24425e+09 |                     2.84552e+09 |            0.2956 |            126.792  |
| ('A', 9)  |              1.12212e+09 |                     1.24804e+09 |            0.153  |            111.221  |
| ('A', 10) |              5.61062e+08 |                     5.20505e+08 |            0.0824 |             92.7713 |
| ('A', 11) |              2.80531e+08 |                     1.83254e+08 |            0.0465 |             65.3237 |

## Sample evaluation

### Sample: controll 'k' 1

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:---------|-----------:|-------------------:|----------------:|:--------------|
| ('A', 1) |     1.554  |                  1 |     1.93599e+10 | >1.795e+10    |
| ('A', 2) |     0.921  |                  2 |     2.14074e+10 |               |
| ('A', 3) |     0.5703 |                  4 |     2.46991e+10 |               |
| ('A', 4) |     0.3327 |                  8 |     2.62344e+10 |               |

CV = 10.2 [%]  
mean = 2.293e+10 [cp/ml]  
valid = True  
note: Ruduced number of sample points. Measured 4, valid 3;>1.795e+10;Measured OD 1.554e+0 > 4.650e-2

!["alt text"](control_01.png)

### Sample: sample 's' 1

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason     |
|:---------|-----------:|-------------------:|----------------:|:----------------|
| ('B', 1) |     0.0146 |                  1 |             nan | Backfit failed. |
| ('B', 2) |     0.0118 |                  2 |             nan | Backfit failed. |
| ('B', 3) |     0.0094 |                  4 |             nan | Backfit failed. |
| ('B', 4) |     0.0081 |                  8 |             nan | Backfit failed. |

CV = nan [%]  
mean = nan [cp/ml]  
valid = False  
note: Not enough valid sample points. Required 2, available 0;Backfit failed.;Measured OD 1.460e-2 < 4.650e-2

![sample_01.png](img/sample_01.png)

### Sample: sample 's' 2

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason     |
|:---------|-----------:|-------------------:|----------------:|:----------------|
| ('C', 1) |     0.0233 |                  1 |             nan | Backfit failed. |
| ('C', 2) |     0.0211 |                  2 |             nan | Backfit failed. |
| ('C', 3) |     0.0112 |                  4 |             nan | Backfit failed. |
| ('C', 4) |     0.0091 |                  8 |             nan | Backfit failed. |

CV = nan [%]  
mean = nan [cp/ml]  
valid = False  
note: Not enough valid sample points. Required 2, available 0;Backfit failed.;Measured OD 2.330e-2 < 4.650e-2

![sample_02.png](img/sample_02.png)

### Sample: sample 's' 3

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason     |
|:---------|-----------:|-------------------:|----------------:|:----------------|
| ('D', 1) |     0.0336 |                  1 |     7.34788e+07 | <2.805e+8       |
| ('D', 2) |     0.0199 |                  2 |   nan           | Backfit failed. |
| ('D', 3) |     0.0138 |                  4 |   nan           | Backfit failed. |
| ('D', 4) |     0.012  |                  8 |   nan           | Backfit failed. |

CV = nan [%]  
mean = 7.348e+07 [cp/ml]  
valid = False  
note: Not enough valid sample points. Required 2, available 0;<2.805e+8, Backfit failed., Backfit failed., Backfit failed.

![sample_03.png](img/sample_03.png)

### Sample: sample 's' 4

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason     |
|:---------|-----------:|-------------------:|----------------:|:----------------|
| ('E', 1) |     0.0133 |                  1 |             nan | Backfit failed. |
| ('E', 2) |     0.0091 |                  2 |             nan | Backfit failed. |
| ('E', 3) |     0.007  |                  4 |             nan | Backfit failed. |
| ('E', 4) |     0.0068 |                  8 |             nan | Backfit failed. |

CV = nan [%]  
mean = nan [cp/ml]  
valid = False  
note: Not enough valid sample points. Required 2, available 0;Backfit failed.;Measured OD 1.330e-2 < 4.650e-2

![sample_04.png](img/sample_04.png)

### Sample: sample 's' 5

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:---------|-----------:|-------------------:|----------------:|:--------------|
| ('F', 1) |     0.8188 |                  1 |     9.35931e+09 |               |
| ('F', 2) |     0.4518 |                  2 |     9.41657e+09 |               |
| ('F', 3) |     0.2265 |                  4 |     8.22226e+09 |               |
| ('F', 4) |     0.1402 |                  8 |     8.895e+09   |               |

CV = 6.16 [%]  
mean = 8.973e+09 [cp/ml]  
valid = True  
![sample_05.png](img/sample_05.png)

### Sample: sample 's' 6

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:---------|-----------:|-------------------:|----------------:|:--------------|
| ('G', 1) |     3.5014 |                  1 |     4.81787e+10 | >1.795e+10    |
| ('G', 2) |     3.0087 |                  2 |     8.13162e+10 | >1.795e+10    |
| ('G', 3) |     2.82   |                  4 |     1.51253e+11 | >1.795e+10    |
| ('G', 4) |     2.2412 |                  8 |     2.33812e+11 | >1.795e+10    |

CV = nan [%]  
mean = 1.286e+11 [cp/ml]  
valid = False  
note: Not enough valid sample points. Required 2, available 0;>1.795e+10;Measured OD 3.501e+0 > 4.650e-2

![sample_06.png](img/sample_06.png)

### Sample: sample 's' 7

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:---------|-----------:|-------------------:|----------------:|:--------------|
| ('H', 1) |     0.991  |                  1 |     1.16344e+10 |               |
| ('H', 2) |     0.5685 |                  2 |     1.23044e+10 |               |
| ('H', 3) |     0.3297 |                  4 |     1.2976e+10  |               |
| ('H', 4) |     0.1539 |                  8 |     1.00614e+10 |               |

CV = 10.6 [%]  
mean = 1.174e+10 [cp/ml]  
valid = True  
![sample_07.png](img/sample_07.png)

### Sample: sample 's' 8

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:---------|-----------:|-------------------:|----------------:|:--------------|
| ('B', 5) |     0.5229 |                  1 |     5.58349e+09 |               |
| ('B', 6) |     0.2986 |                  2 |     5.76073e+09 |               |
| ('B', 7) |     0.1617 |                  4 |     5.36577e+09 |               |
| ('B', 8) |     0.091  |                  8 |     4.84415e+09 |               |

CV = 7.37 [%]  
mean = 5.389e+09 [cp/ml]  
valid = True  
![sample_08.png](img/sample_08.png)

### Sample: sample 's' 9

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason     |
|:---------|-----------:|-------------------:|----------------:|:----------------|
| ('C', 5) |     0.1337 |                  1 |     1.04335e+09 |                 |
| ('C', 6) |     0.0616 |                  2 |     6.41852e+08 |                 |
| ('C', 7) |     0.0357 |                  4 |     3.62526e+08 | <2.805e+8       |
| ('C', 8) |     0.0209 |                  8 |   nan           | Backfit failed. |

CV = 33.7 [%]  
mean = 6.826e+08 [cp/ml]  
valid = False  
note: CV > 0.2; Ruduced number of sample points. Measured 4, valid 2;<2.805e+8, Backfit failed.

![sample_09.png](img/sample_09.png)

### Sample: sample 's' 10

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason     |
|:---------|-----------:|-------------------:|----------------:|:----------------|
| ('D', 5) |     0.0654 |                  1 |     3.56649e+08 |                 |
| ('D', 6) |     0.035  |                  2 |     1.69749e+08 | <2.805e+8       |
| ('D', 7) |     0.0223 |                  4 |   nan           | Backfit failed. |
| ('D', 8) |     0.0151 |                  8 |   nan           | Backfit failed. |

CV = nan [%]  
mean = 2.632e+08 [cp/ml]  
valid = False  
note: Not enough valid sample points. Required 2, available 1;<2.805e+8, Backfit failed., Backfit failed.

![sample_10.png](img/sample_10.png)

### Sample: sample 's' 11

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:---------|-----------:|-------------------:|----------------:|:--------------|
| ('E', 5) |     2.2784 |                  1 |     2.97715e+10 | >1.795e+10    |
| ('E', 6) |     1.6191 |                  2 |     4.05529e+10 | >1.795e+10    |
| ('E', 7) |     1.1646 |                  4 |     5.58961e+10 |               |
| ('E', 8) |     0.7127 |                  8 |     6.38701e+10 |               |

CV = 9.42 [%]  
mean = 4.752e+10 [cp/ml]  
valid = True  
note: Ruduced number of sample points. Measured 4, valid 2;>1.795e+10;Measured OD 2.278e+0 > 4.650e-2

![sample_11.png](img/sample_11.png)

### Sample: sample 's' 12

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason     |
|:---------|-----------:|-------------------:|----------------:|:----------------|
| ('F', 5) |     0.0131 |                  1 |             nan | Backfit failed. |
| ('F', 6) |     0.0092 |                  2 |             nan | Backfit failed. |
| ('F', 7) |     0.0083 |                  4 |             nan | Backfit failed. |
| ('F', 8) |     0.009  |                  8 |             nan | Backfit failed. |

CV = nan [%]  
mean = nan [cp/ml]  
valid = False  
note: Not enough valid sample points. Required 2, available 0;Backfit failed.;Measured OD 1.310e-2 < 4.650e-2

![sample_12.png](img/sample_12.png)

### Sample: sample 's' 13

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason     |
|:---------|-----------:|-------------------:|----------------:|:----------------|
| ('G', 5) |     0.0097 |                  1 |             nan | Backfit failed. |
| ('G', 6) |     0.0078 |                  2 |             nan | Backfit failed. |
| ('G', 7) |     0.0083 |                  4 |             nan | Backfit failed. |
| ('G', 8) |     0.0084 |                  8 |             nan | Backfit failed. |

CV = nan [%]  
mean = nan [cp/ml]  
valid = False  
note: Not enough valid sample points. Required 2, available 0;Backfit failed.;Measured OD 9.700e-3 < 4.650e-2

![sample_13.png](img/sample_13.png)

### Sample: sample 's' 14

|          |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:---------|-----------:|-------------------:|----------------:|:--------------|
| ('H', 5) |     1.5486 |                  1 |     1.92841e+10 | >1.795e+10    |
| ('H', 6) |     1.0657 |                  2 |     2.52718e+10 |               |
| ('H', 7) |     0.668  |                  4 |     2.9644e+10  |               |
| ('H', 8) |     0.4213 |                  8 |     3.47007e+10 |               |

CV = 15.8 [%]  
mean = 2.723e+10 [cp/ml]  
valid = True  
note: Ruduced number of sample points. Measured 4, valid 3;>1.795e+10;Measured OD 1.549e+0 > 4.650e-2

![sample_14.png](img/sample_14.png)

### Sample: sample 's' 15

|           |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:----------|-----------:|-------------------:|----------------:|:--------------|
| ('B', 9)  |     1.8693 |                  1 |     2.38365e+10 | >1.795e+10    |
| ('B', 10) |     1.2447 |                  2 |     3.01345e+10 |               |
| ('B', 11) |     0.8001 |                  4 |     3.64613e+10 |               |
| ('B', 12) |     0.4515 |                  8 |     3.7637e+10  |               |

CV = 11.6 [%]  
mean = 3.202e+10 [cp/ml]  
valid = True  
note: Ruduced number of sample points. Measured 4, valid 3;>1.795e+10;Measured OD 1.869e+0 > 4.650e-2

![sample_15.png](img/sample_15.png)

### Sample: sample 's' 16

|           |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:----------|-----------:|-------------------:|----------------:|:--------------|
| ('C', 9)  |     0.7849 |                  1 |     8.91747e+09 |               |
| ('C', 10) |     0.3998 |                  2 |     8.15627e+09 |               |
| ('C', 11) |     0.254  |                  4 |     9.46752e+09 |               |
| ('C', 12) |     0.1339 |                  8 |     8.36359e+09 |               |

CV = 6.76 [%]  
mean = 8.726e+09 [cp/ml]  
valid = True  
![sample_16.png](img/sample_16.png)

### Sample: sample 's' 17

|           |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:----------|-----------:|-------------------:|----------------:|:--------------|
| ('D', 9)  |     1.4741 |                  1 |     1.82409e+10 | >1.795e+10    |
| ('D', 10) |     0.8847 |                  2 |     2.04483e+10 |               |
| ('D', 11) |     0.5683 |                  4 |     2.45988e+10 |               |
| ('D', 12) |     0.3198 |                  8 |     2.50222e+10 |               |

CV = 10.8 [%]  
mean = 2.208e+10 [cp/ml]  
valid = True  
note: Ruduced number of sample points. Measured 4, valid 3;>1.795e+10;Measured OD 1.474e+0 > 4.650e-2

![sample_17.png](img/sample_17.png)

### Sample: sample 's' 18

|           |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:----------|-----------:|-------------------:|----------------:|:--------------|
| ('E', 9)  |     0.907  |                  1 |     1.05185e+10 |               |
| ('E', 10) |     0.5332 |                  2 |     1.14229e+10 |               |
| ('E', 11) |     0.2803 |                  4 |     1.06739e+10 |               |
| ('E', 12) |     0.1603 |                  8 |     1.06109e+10 |               |

CV = 3.85 [%]  
mean = 1.081e+10 [cp/ml]  
valid = True  
![sample_18.png](img/sample_18.png)

### Sample: sample 's' 19

|           |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:----------|-----------:|-------------------:|----------------:|:--------------|
| ('F', 9)  |     0.792  |                  1 |     9.00983e+09 |               |
| ('F', 10) |     0.4611 |                  2 |     9.64381e+09 |               |
| ('F', 11) |     0.2491 |                  4 |     9.24438e+09 |               |
| ('F', 12) |     0.1442 |                  8 |     9.23406e+09 |               |

CV = 2.84 [%]  
mean = 9.283e+09 [cp/ml]  
valid = True  
![sample_19.png](img/sample_19.png)

### Sample: sample 's' 20

|           |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:----------|-----------:|-------------------:|----------------:|:--------------|
| ('G', 9)  |     0.5592 |                  1 |     6.03578e+09 |               |
| ('G', 10) |     0.334  |                  2 |     6.58921e+09 |               |
| ('G', 11) |     0.1677 |                  4 |     5.62497e+09 |               |
| ('G', 12) |     0.0936 |                  8 |     5.05171e+09 |               |

CV = 11.2 [%]  
mean = 5.825e+09 [cp/ml]  
valid = True  
![sample_20.png](img/sample_20.png)

### Sample: sample 's' 21

|           |   OD_delta |   plate_layout_dil |   concentration | mask_reason   |
|:----------|-----------:|-------------------:|----------------:|:--------------|
| ('H', 9)  |     0.6562 |                  1 |     7.26053e+09 |               |
| ('H', 10) |     0.3631 |                  2 |     7.27814e+09 |               |
| ('H', 11) |     0.2077 |                  4 |     7.38145e+09 |               |
| ('H', 12) |     0.1284 |                  8 |     7.90237e+09 |               |

CV = 4.06 [%]  
mean = 7.456e+09 [cp/ml]  
valid = True  
![sample_21.png](img/sample_21.png)

