# Import required libraries
import pandas as pd
import numpy as np
 
# Set random seed for reproducibility
np.random.seed(42)

# Generate baseline metrics (Month 0 - before intervention)
print("\n[Step 3/6] Generating baseline metrics...")

# Import file
branches_with_study_groups = pd.read_csv('02_data/branches_with_study_groups.csv')
 
# Generate baseline metrics
baseline_metrics = []
 
# Extract branch code and population from the dataframe of branches
for _, branch in branches_with_study_groups.iterrows():
    branch_code = branch['branch_code']
    student_population = branch['student_population']
# Create baseline data
    baseline_metrics.append({
        'branch_code': branch_code,
        'measurement_period': 'baseline',
 
        #Create the pass percentage using the normal distribution because:
        #pass percentage revolves around a mean with some sd
        'pass_percentage': round(np.clip(np.random.normal(70, 5), 0, 100),2), #percentage remains between 0 and 100
        
        #Create new_enrollments using Poisson distribution  because:
        # new enrollments are discrete and
        #usually occur at a smooth rate (but randomly) w.r.t. the current students' population
        'new_enrollments': int(np.random.poisson(0.3 * student_population)),
 
        #Create revenue for branches using lognormal distribution because:
        #Revenue can't be negative, it is right-skewed, some branches make much more revenue than others
        'revenue': round(np.random.lognormal(np.log(student_population * 500), 0.15),2),
        
        #Create the cleanliness score using uniform distribution because:
        #Cleanliness level of most of the branches remains around average
        # usually not less than 30 and more than 100
        'cleanliness_score': round(np.clip(np.random.normal(60, 10), 30, 100),2), 
        'measurement_date': '2023-01-01'
    })
# Convert to a dataframe
baseline_df =pd.DataFrame(baseline_metrics)
print(f"\n Generated {len(baseline_df)} baseline records\n")
print(baseline_df.head())

# Generate Year 1 metrics (Month 12 - after intervention)
print("\n[Step 4/6] Generating Year 1 metrics...")

# Different improvements based on study groups 
year1_metrics = []

for _, branch in branches_with_study_groups.iterrows():
 branch_code = branch['branch_code']
 study_group = branch['study_group']

 # Get baseline values for branch 
 baseline = baseline_df[baseline_df['branch_code'] == branch_code].iloc[0]

 # Different improvement based on study group
 if study_group == 'experimental':
    pass_improvement = np.random.uniform(6, 10)  # 6 to 10 points
    enroll_growth = np.random.uniform(1.08, 1.1) # 8% to 10% growth
    revenue_growth = np.random.uniform(1.08, 1.15) # 8% to 15% growth
    clean_improvement = np.random.uniform(8, 12)  # 8 to 12 points

 elif study_group == 'control':
    pass_improvement = np.random.uniform(2, 7) # 2 to 7 points
    enroll_growth = np.random.uniform(1.0, 1.05) # 0% to 5% growth
    revenue_growth = np.random.uniform(1.03, 1.09) # 3% to 9% growth
    clean_improvement = np.random.uniform(3, 7)  # 3 to 7 points

 else: # for branches not selected
    pass_improvement = np.random.uniform(1, 7) # 1 to 7 points
    enroll_growth = np.random.uniform(1.0, 1.06) # 0% to 6% growth
    revenue_growth = np.random.uniform(1.02, 1.08) # 2% to 8% growth
    clean_improvement = np.random.uniform(3, 8) # 3 to 8 points

# Calculate year 1 values
 year1_metrics.append({
 'branch_code' : branch['branch_code'],
 'measurement_period' : 'year 1',
 'pass_percentage': round(min(100, baseline['pass_percentage'] + pass_improvement), 2),
 'new_enrollments': int(baseline['new_enrollments'] * enroll_growth),
 'revenue': round(baseline['revenue'] * revenue_growth, 2),
 'cleanliness_score': round(min(100, baseline['cleanliness_score'] + clean_improvement), 2),
 'measurement_date': '2024-01-01'
   })
year1_df = pd.DataFrame(year1_metrics)
print(year1_df.head())
print(f'{len(year1_df)} records generated')

# Save files in cvs format
baseline_df.to_csv('02_data/baseline_df.csv', index=False)
year1_df.to_csv('02_data/year1_df.csv', index=False)