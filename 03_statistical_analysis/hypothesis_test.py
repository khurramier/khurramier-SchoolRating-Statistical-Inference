# Import required libraries
import pandas as pd
import numpy as np
from scipy import stats
 
# Set random seed for reproducibility
np.random.seed(42)

# Conduct hypothesis test
print("\n[Step 6/6] Conducting hypothesis test...")

#import file
comp_df = pd.read_csv('02_data/composite_df')

# Separate experimental and control
experimental = comp_df[comp_df['study_group']=='experimental']['composite_score']
control = comp_df[comp_df['study_group']=='control']['composite_score']
 
# Display stats
print(f"\n{'=' * 70}\n")
print('SUMMARY STATISTICS(EXPERIMENTAL VS CONTROL GROUP)')
print(f"\n{'=' * 70}")
 
print(f"\nExperimental Group (n={len(experimental)}):")
print(f"  Mean:     {experimental.mean():.2f}")
print(f"  Median:   {experimental.median():.2f}")
print(f"  Std Dev:  {experimental.std():.2f}")
print(f"  Min:      {experimental.min():.2f}")
print(f"  Max:      {experimental.max():.2f}")
 
print(f"\nControl Group (n={len(control)}):")
print(f"  Mean:     {control.mean():.2f}")
print(f"  Median:   {control.median():.2f}")
print(f"  Std Dev:  {control.std():.2f}")
print(f"  Min:      {control.min():.2f}")
print(f"  Max:      {control.max():.2f}")
 
# Display difference in mean
diff_means = experimental.mean() - control.mean()
print(f'Difference in means is {diff_means:.2f}')
 
# Hypothesis Test
print('=' * 90)
print ('HYPOTHESIS TEST')
print('=' * 90)
print('\nNULL HYPOTHESIS: There is no effect of implementation of branch rating sytem.')
print('\nMean(Experimental) = Mean(Control)')
print("\nALTERNATE HYPOTHESIS: Implementation of branch rating system improves branches' performance\n")
print('Mean(Experimental) > Mean(Control)')
print('=' * 90)
 
# independent sample t-test(two-tailed)
t_stats, p_value_two_tailed = stats.ttest_ind(experimental, control)
# convert two-tailed to one-tailed
p_value_one_tailed = p_value_two_tailed/2
 
# Print the test results
print("\n" + "-"*70)
print("TEST RESULTS")
print("-"*70)
print(f"t-statistic:        {t_stats:.4f}")
print(f"p-value (one-tail): {p_value_one_tailed:.4f}")
print(f"Significance level: alpha = 0.05")
 
# Conclusion
print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
 
if p_value_one_tailed < 0.001:
    significance_level = "highly significant (p < 0.001)"
elif p_value_one_tailed < 0.05:
    significance_level = "significant (p < 0.05)"
else:
    significance_level = "not significant (p ≥ 0.05)"
 
print(f"\nThe difference of {diff_means:.2f} points is {significance_level}.")
 
if p_value_one_tailed < 0.05:
    print(f"\nREJECT the null hypothesis")
    print(f"\nThere is strong statistical evidence that the rating system")
    print(f"    IMPROVES branch performance.")
    print(f"\n  BUSINESS RECOMMENDATION:")
    print(f"  Implement the rating system across all 400 branches.")
else:
    print(f"\n FAIL TO REJECT the null hypothesis")
    print(f"\nInsufficient evidence that the rating system has an effect.")
    print(f"\nBUSINESS RECOMMENDATION:")
    print(f"Do NOT implement the rating system (no proven benefit).")