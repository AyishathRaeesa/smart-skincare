#LAB_5
import numpy as np
import scipy.stats as stats
n = int(input("Enter sample size (n): "))
sample_mean = float(input("Enter sample mean: "))
sample_std = float(input("Enter sample standard deviation: "))
mu0 = float(input("Enter population mean under H0 (e.g., 0): "))
alpha = float(input("Enter significance level (e.g., 0.05): "))
t = (sample_mean - mu0) / (sample_std / np.sqrt(n))
df = n-1
critical_t = stats.t.ppf(1-alpha/2, df)
p_value = 2 * (1 - stats.t.cdf(np.abs(t), df))
print("\n--- Hypothesis Test Results ---")
print(f"t-statistic: {t:.4f}")
print(f"Critical t-value: {critical_t:.4f}")
print(f"Degrees of freedom: {df}")
print(f"p-value: {p_value:.4f}")
if(np.abs(t) > critical_t):
    print("Reject the null hypothesis")
else:
    print("Accept the null hypothesis")