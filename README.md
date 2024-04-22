# 8451 Data Analysis Documentation

Authors: Arya Narke, Ameya Deshmukh, Om Gaikwad

## Overview
This repository contains documentation, data files, and code for analyzing customer engagement data. The analysis focuses on understanding the factors influencing customer engagement, including category growth or decline and the impact of demographic factors.

## Contents
- [Questions](#questions)
- [Tasks](#tasks)
- [Code Explanation](#code-explanation)
- [Answering the Questions](#answering-the-questions)

## Questions
### Question 1
What categories are growing or shrinking with changing customer engagement?

### Question 2
Which demographic factors (e.g. household size, presence of children, income) appear to affect customer engagement?

## Tasks
### TASK 1: ML Write-up
- Explanation of Linear Regression, Random Forest, and Gradient Boosting Algorithms.
- Predictive Modeling Technique Selection.

### TASK 2: Launch web server
- Configuration of web server using Google Compute Engine and Google Cloud SQL.

### TASK 3: Create Database and Sample Data Pull for HSHD_NUM #10
- Importing data from Google Storage Buckets to Google Cloud SQL.
- Data analysis using pandas dataframe.

### TASK 4: Search Based on HSHD_NUM

### TASK 5: Dashboard with Plot and Answer
- Analysis of customer engagement.
- Correlation coefficient calculation.
- Interpretation of results.

### TASK 6: Load Datasets
- Loading sample datasets for testing.

## Code Explanation
### Data Loading and Preprocessing
- Loading datasets: households, products, and transactions.
- Preprocessing steps: handling missing values, data type conversion, one-hot encoding.

### Building and Evaluating Linear Regression Model
- Training and evaluation of a linear regression model.
- Visualization of model performance.

### Analyzing Feature Coefficients
- Extraction and analysis of feature coefficients.
- Identification of top features affecting customer engagement.

### Analyzing Category Coefficients
- Analysis of coefficients associated with categories to determine growth or decline.

## Answering the Questions
### What categories are growing or shrinking with changing customer engagement?
- Analysis of category coefficients to identify growing or shrinking categories.

### Which demographic factors appear to affect customer engagement?
- Utilization of linear regression model to analyze the impact of demographic factors.
- Extraction and analysis of feature coefficients.
