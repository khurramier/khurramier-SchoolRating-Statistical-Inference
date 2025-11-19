# Import required libraries
import pandas as pd
import numpy as np
from scipy import stats
 
# Set random seed for reproducibility
np.random.seed(42)
 
# Display introduction of Project
print("="*70)
print("SCHOOL BRANCH RATING SYSTEM - HYPOTHESIS TESTING ANALYSIS")
print("="*70)
print("\n Libraries imported")
print(" Random seed set to 42 for reproducibility")
# Generate 400 branches
print("\n[Step 1/6] Generating 400 branch records...")

# Create an empty list to hold branch data
branches =[]
#generate branch data using a loop
for i in range(1, 401):
 #branch codes from B001 to B400
 branch_code = f"B{i:03d}" 

    #randomly assign location
 location = pd.Series(np.random.choice(['rural', 'urban'])) 

#randomly assign student population. less for rural, more for urban
 if(location[0] == 'rural'):
    student_population = pd.Series(np.random.randint(50, 200))
 else:
    student_population = pd.Series(np.random.randint(100, 500))
#randomly assign region
 region = pd.Series(np.random.choice(['Punjab', 'KPK', 'Sind', 'Balochistan']))
# establishment year between 2010-2020
 establishment_year = np.random.randint(2010, 2020)
#append branch data to list    
 branches.append({'branch_code': branch_code,
                   'location': location[0], 
                   'student_population': student_population[0], 
                   'region': region[0], 
                   'establishment_year': establishment_year})
branches_df= pd.DataFrame(branches) 
# Categorize branches based on student population
branches_df['size_category'] = np.where(branches_df['student_population'] < 150, 'small',
np.where(branches_df['student_population'] < 300, 'medium', 'large'))
print(f"Sample of branches DataFrame: of {len(branches_df)} branches")
print(branches_df.head())
print(f"\nLocation distribution:")
print(branches_df['location'].value_counts())
# Saving the file in csv format
branches_df.to_csv(r'02_data\branches.csv')