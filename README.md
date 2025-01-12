# grade-curve

### Introduction
This curves raw grades without any preferential treatment to any identifiable student.  The grade curving transform is linear:

$$y = f(x; \varepsilon) = \varepsilon x_0 + \bigg ( \frac{x - x_0}{x_1 - x_0} \bigg ) \times (100 - \varepsilon x_0),$$

where $y$ is the curved grade corresponding to the raw grade $x$, $f(\cdot; \cdot)$ is the transform with a parameter $\varepsilon$ that controls the generousity (or penalty) of the transform, $x_0 := \min x$ is the least raw grade in class, and $x_1 := \max x$ is the highest raw grade in class (the maximum grade cannot exceed $100$).

### Prequisite
Before using the code, ensure that the correct cutoff per the syllabus has been programmed.  For example, this is a five-point scale:
```
  df_syllabus = pd.DataFrame(data={'letter': ['A', 'B', 'C', 'D', 'F'],
                                     'upper': [100.00, 89.99, 79.99, 69.99, 59.99]})
```

The code uses `numpy`, `pandas`, and `matplotlib` libraries (no check has been made on the minimum compatible version).

### Benefits
Unlike traditional scaling methods, this methodology brings forward the following benefits:

1. It does not require any assumption about the statistical distribution of the grades prior to curving (e.g., a Normal distribution).
2. The least performing student can also benefit from the transform to boost their grade.
3. The code does not transform the statistical distribution of the grades.  Only the mean and variance of the distribution of the curved grades are impacted (these can be straightforward computed as $\mathbb{E}[y]$ and $\text{Var}[y]$ from the transform above).

### Output
```
Before curving:
---------------
Lowest grade: 46.52.
Highest grade: 96.12.
Mean (+/- std): 74.54 (+/- 14.92).
Median: 77.92 (C).
--------------------------------------------------------------------------------

After curving (epsilon = 0.05):
-------------------------------
Lowest grade: 48.85.
Highest grade: 100.0.
Mean (+/- std): 77.75 (+/- 15.38).
Median: 81.23 (B).
--------------------------------------------------------------------------------
```
![](https://github.com/farismismar/grade-curve/blob/main/plot.png)

### Version
Version | Date | Description
| ------------- |:-------------:| :-----|
| 0.1      | 2025-01-12 | First release. |
