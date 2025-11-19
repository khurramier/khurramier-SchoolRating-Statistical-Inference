# Import required libraries
import pandas as pd
import numpy as np
from scipy import stats
 
# Set random seed for reproducibility
np.random.seed(42)

# Calculate improvements and composite score
print("\n[Step 5/6] Calculating improvements and composite scores...")

# Import files
baseline_df = pd.read_csv('02_data/baseline_df.csv')
year1_df = pd.read_csv('02_data/year1_df.csv')
branches_with_study_groups = pd.read_csv('02_data/branches_with_study_groups.csv')
# Merge baseline and year1
improvements = baseline_df.merge(
year1_df,
on='branch_code',suffixes=('_baseline', '_year1')
)
print('year 1 and baseline')
print (improvements.head())
# Merge with branches dataframe
improvements = improvements.merge(
branches_with_study_groups[['branch_code', 'study_group']],
on='branch_code'
)

# Calculate improvements
improvements['pass_improvement'] = improvements['pass_percentage_year1']- improvements['pass_percentage_baseline']

improvements['enroll_growth_pct'] = (improvements['new_enrollments_year1'] - improvements['new_enrollments_baseline'])/improvements['new_enrollments_baseline'] * 100

improvements['revenue_growth_pct'] = (improvements['revenue_year1'] - improvements['revenue_baseline'])/improvements['revenue_baseline'] * 100

improvements['cleanliness_improvement'] = improvements['cleanliness_score_year1'] - improvements['cleanliness_score_baseline']

# Calculate composite score with weights
# Define weights as per school policy
weights = {
 'pass_improvement': 0.30,
 'enroll_growth_pct': 0.25,
 'revenue_growth_pct': 0.25,
 'cleanliness_improvement': 0.20
}
# Calculate composite score
improvements['composite_score'] = (
weights['pass_improvement'] * improvements['pass_improvement'] +
weights['enroll_growth_pct'] * improvements['enroll_growth_pct'] +
weights['revenue_growth_pct'] * improvements['revenue_growth_pct'] +
weights['cleanliness_improvement'] * improvements['cleanliness_improvement']
)
# Filter to study groups only
composite_df = improvements[improvements['study_group'].isin(['experimental', 'control'])]

print(f" Calculated composite scores for {len(composite_df)} branches")
print(f"\nWeights: Pass(30%), Enrollment(25%), Revenue(25%), Cleanliness(20%)")
print(f"\nComposite score by group:")
print(composite_df.groupby('study_group')['composite_score'].describe())

#Save file as csv
composite_df.to_csv('02_data/composite_df')