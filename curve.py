#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 12:53:03 2025

@author: farismismar
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

utd_green = '#154734'
utd_orange = '#e87500'

# System parameters
scenario = '5-point'        # '12-point' or '5-point'
epsilon = 0.0005            # how generous (higher epsilon is better)
before_color = utd_green
after_color = utd_orange

##############################################################################
assert(scenario in ['12-point', '5-point'])

## Load the file rounded up to two decimals
df = pd.read_csv('grades.csv')
df['Grade'] = df['Grade'].apply(lambda x: np.round(x, 2))

if df.isnull().sum().sum() != 0:
    raise RuntimeError("Ensure all values have scores.  No missing data is allowed.")
   
## Load the syllabus cutoff thresholds.
if scenario == '12-point':
    df_syllabus = pd.DataFrame(data={'letter': ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D-', 'D', 'F'],
                                     'upper': [100.00, 89.99, 86.66, 83.33, 79.99, 76.66, 73.33, 69.99, 66.66, 63.33, 59.99, 56.66]})
elif scenario == '5-point':
    df_syllabus = pd.DataFrame(data={'letter': ['A', 'B', 'C', 'D', 'F'],
                                     'upper': [100.00, 89.99, 79.99, 69.99, 59.99]})
else:
    False  # This line is not going to be executed.

df_syllabus['upper'].apply(lambda x: np.round(x, 2))
df_syllabus = df_syllabus.sort_values(by='upper', ascending=True).reset_index(drop=True)
letters = df_syllabus['letter']
bins = [0] + df_syllabus['upper'].to_list() 

lowest_grade = df['Grade'].min()
highest_grade = df['Grade'].max()
mean_grade = np.round(df['Grade'].mean(), 2)
std_grade = np.round(df['Grade'].std(), 2)
median_grade = np.round(df['Grade'].median(), 2)
median_letter = pd.cut([median_grade], bins=bins, labels=letters, right=True)[0]

df['letter'] = pd.cut(df['Grade'], bins=bins, labels=letters, right=True)

if epsilon < 0:
    print('*' * 80)
    print(f'Warning:  This value of epsilon ({epsilon}) will penalize students!')
    print('*' * 80)
    print()
          
## Apply curve (linear transform)
bias = (1 + epsilon) * lowest_grade
multiplier = 100 - bias

df['curved_grade'] = bias + ((df['Grade'] - lowest_grade) / (highest_grade - lowest_grade)) * multiplier
df['curved_grade'] = df['curved_grade'].apply(lambda x: np.round(x, 2))
df['curved_letter'] = pd.cut(df['curved_grade'], bins=bins, labels=letters, right=True)

lowest_curved_grade = df['curved_grade'].min()
highest_curved_grade = df['curved_grade'].max()
mean_curved_grade = np.round(df['curved_grade'].mean(), 2)
std_curved_grade = np.round(df['curved_grade'].std(), 2)
median_curved_grade = np.round(df['curved_grade'].median(), 2)
median_curved_letter = pd.cut([median_curved_grade], bins=bins, labels=letters, right=True)[0]

##
print('Before curving:')
print('-' * 15)
print(f'Lowest grade: {lowest_grade}.')
print(f'Highest grade: {highest_grade}.')
print(f'Mean (+/- std): {mean_grade} (+/- {std_grade}).')
print(f'Median: {median_grade:.2f} ({median_letter}).')
print('-' * 80)
print()
print(f'After curving (epsilon = {epsilon:.2f}):')
print('-' * 31)
print(f'Lowest grade: {lowest_curved_grade}.')
print(f'Highest grade: {highest_curved_grade}.')
print(f'Mean (+/- std): {mean_curved_grade} (+/- {std_curved_grade}).')
print(f'Median: {median_curved_grade:.2f} ({median_curved_letter}).')
print('-' * 80)
    
## Build histograms
plt.rcParams["font.family"] = "Arial"

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

df["letter"].value_counts(sort=False).reindex(sorted(df_syllabus['letter'])).plot(
    kind='bar', color=before_color, edgecolor='none', ax=ax1)

df["curved_letter"].value_counts(sort=False).reindex(sorted(df_syllabus['letter'])).plot(
    kind='bar', color=after_color, edgecolor='none', ax=ax2)

# Ensure y-axis labels are integers
ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

# Add labels and title
ax1.set_xlabel('Letter Grade (raw)')
ax2.set_xlabel('Letter Grade (curved)')

ax1.set_ylabel('Number of Students')
ax2.set_ylabel('Number of Students')

ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0, ha='right')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0, ha='right')

ax1.grid(axis='y', alpha=0.7)
ax2.grid(axis='y', alpha=0.7)

# Show the plot
plt.tight_layout()
plt.show()
plt.close(fig)