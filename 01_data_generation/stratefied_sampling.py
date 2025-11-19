# Import required libraries
import pandas as pd
import numpy as np
 
# Set random seed for reproducibility
np.random.seed(42)

# Perform stratified sampling (50 experimental + 50 control)
print("\n[Step 2/6] Performing stratified sampling...")

# Import file
branches_df = pd.read_csv('02_data/branches.csv')
# Make stratum for sampling
# Give due representation to the region, location, and size of branches
branches_df['stratum'] = branches_df['region'] + '_' + branches_df['location'] + '_'+ branches_df['size_category']
print('='*70)
print('STRATA BASED ON REGION, LOCATION AND SIZE')
print('='*70)
# Display stratum counts to calculate proportional sample sizes per stratum
stratum_counts = branches_df['stratum'].value_counts()
print(stratum_counts)
print(f'Total Strata: {len(stratum_counts)}')

# Calculate sample sizes per stratum for Stratified Sampling (50 branches)
sample_size_per_stratum = {}
for stratum, count in stratum_counts.items():
 sample_size = max(1, int(count/400 * 50))
 sample_size_per_stratum[stratum] = sample_size
total_sampled = sum(sample_size_per_stratum.values())
# Count how many more branches are required to complete the sample (50 branches)
if total_sampled < 50:
 remaining_required_branches = 50 - total_sampled
else:
 remaining_required_branches = 0
print('-' * 110)
print(f'Out of 50 branches to be sampled, {total_sampled} will be selected using stratified sampling technique across {len(stratum_counts)} strata ')
print(f'while the remaining {remaining_required_branches} will be chosen through simple random sampling.')

# Sample branches for experimental sample using stratified sampling 
experimental_dfs = []
for str_exp, count_exp in sample_size_per_stratum.items():
 experimental_branches = branches_df[branches_df['stratum']== str_exp]
 sampled_exp = experimental_branches.sample(n=count_exp, random_state=42)
 experimental_dfs.append(sampled_exp)
experimental_sample = pd.concat(experimental_dfs)

# Sample remaining branches for experimental sample
# Find rows other than those included in the experimental sample
available_rows = branches_df[~branches_df['branch_code'].isin(experimental_sample['branch_code'])]
# select branches using the simple random sampling
remaining_exp_branches = available_rows.sample(n=remaining_required_branches, random_state=42)
# add remaining branches to the experimental group to complete the sample of 50 branches
experimental_sample = pd.concat([experimental_sample, remaining_exp_branches])

#Sample for Control Group
# Exclude branches included in experimental sample
df_remaining_after_exp_sample = branches_df[~branches_df['branch_code'].isin(experimental_sample['branch_code'])]

# Sample branches for the control sample using stratified sampling
control_dfs = []
for str_cont, count_cont in sample_size_per_stratum.items():
 control_branches = df_remaining_after_exp_sample[df_remaining_after_exp_sample['stratum']==str_cont]
 sampled_control = control_branches.sample(n=count_cont, random_state=42)
 control_dfs.append(sampled_control)
control_sample = pd.concat(control_dfs)

# Sample remaining branches for control sample
available_rows_4_control_sample = df_remaining_after_exp_sample[~df_remaining_after_exp_sample['branch_code'].isin(control_sample['branch_code'])]
remaining_contorl_branches= available_rows_4_control_sample.sample(n=remaining_required_branches, random_state=42)
control_sample = pd.concat([control_sample, remaining_contorl_branches])

#reset indices of experimental and control sample dataframes
experimental_sample= experimental_sample.reset_index(drop=True)
print('-'*70)
print('EXPERIMENTAL BRANCHES: SAMPLE')
print(experimental_sample.head())
print('-'*70)

control_sample = control_sample.reset_index(drop=True)
print('CONTROL BRANCHES: SAMPLE')
print(control_sample.head())
# Update the branches dataframe with column study_group

# Make dataframe of 'branches not selected' in exp/cont groups
df_remaining_rows_after_sampling = available_rows_4_control_sample[~available_rows_4_control_sample['branch_code'].isin(control_sample['branch_code'])].copy()

# adding study_group columns to experimental/control sample and 'branches not selected'
experimental_sample['study_group'] = 'experimental'
control_sample['study_group'] = 'control'
df_remaining_rows_after_sampling['study_group'] = 'not selected'
branches_with_study_groups = pd.concat([experimental_sample, control_sample, df_remaining_rows_after_sampling])
print('*' * 70)
print("UPDATED BRANCHES'S DATAFRAME: SAMPLE" )
print('*' * 70)
print(branches_with_study_groups.tail())
print('Status of')
print(branches_with_study_groups['study_group'].value_counts())

# Save as csv file 
branches_with_study_groups.to_csv('02_data/branches_with_study_groups.csv', index=False)