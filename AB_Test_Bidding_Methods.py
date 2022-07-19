
################################################
# Task 1: Preparing and Analyzing Data
################################################

# Step 1: Let's read the data set ab_testing_data.xlsx consisting of control and test group data.
# Let's assign control and test group data to separate variables.


import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene, ttest_ind


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

dataframe_control = pd.read_excel("../AB_Test_Bidding_Methods/ab_testing.xlsx" , sheet_name="Control Group")
dataframe_test = pd.read_excel("../AB_Test_Bidding_Methods/ab_testing.xlsx" , sheet_name="Test Group")

df_control = dataframe_control.copy()
df_test = dataframe_test.copy()

# Step 2: Let's analyze the control and test group data.


def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head())
    print("##################### Tail #####################")
    print(dataframe.tail())
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df_control)
check_df(df_test)


# Step 3: After the analysis, let's combine the control and test group data using the concat method.

df_control["group"] = "control"
df_test["group"] = "test"

df = pd.concat([df_control,df_test], axis=0,ignore_index=False)
df.head()





################################################
# Task 2: Define A/B Test Hypothesis
################################################

# Step 1: Let's define the hypothesis.

# H0 : M1 = M2 (There is no difference between the control group and test group purchasing averages.)
# H1 : M1!= M2 (There is a difference between the purchasing averages of the control group and test group.)


# Step 2: Let's analyze the averages of purchases for the control and test group.

df.groupby("group").agg({"Purchase": "mean"})

###############################################
# TASK 3: Performing Hypothesis Testing
###############################################

# Step 1: Checking the assumptions before testing the hypothesis. These are Assumption of Normality and Homogeneity of Variance.

# Testing whether the control and test groups comply with the normality assumption separately via the Purchase variable.
# Normality Assumption:
# H0: Normal distribution assumption is provided.
# H1: Normal distribution assumption not provided

# p < 0.05 H0 RED
# p > 0.05 H0 CANNOT BE REJECTED

# Let's check whether the normality assumption is provided for the control and test groups according to the test result 
# and interpret the obtained p-values.


test_stat, pvalue = shapiro(df.loc[df["group"] == "control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value=0.5891
# HO cannot be denied. The values of the control group provide the assumption of normal distribution.


# Variance Homogeneity :
# H0: Variances are homogeneous.
# H1: Variances are not homogeneous.
# p < 0.05 H0 RED
# p > 0.05 H0 CANNOT BE REJECTED
# Let's test whether homogeneity of variance is provided for the control and test groups, over the Purchase variable.
# Let's check whether the assumption of normality is provided according to the test result and interpret the obtained p-values.

test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value=0.1083
# HO cannot be denied. The values of the Control and Test groups provide the assumption of variance homogeneity.
# Variances are Homogeneous.


# Step 2: Let's choose the appropriate test based on the Normality Assumption and Variance Homogeneity results.

# Since assumptions are provided, independent two-sample t-test (parametric test) is performed.
# H0: M1 = M2 (There is no mean difference between the control group and test group purchase mean.)
# H1: M1 != M2 (There is a mean difference between the control group and test group purchase mean)
# p<0.05 HO RED , p>0.05 HO CANNOT BE REJECTED

test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Step 3: Considering the p_value obtained as a result of the test, 
# let's interpret whether there is a statistically significant difference between the purchasing averages of the control and test group.

# p-value=0.3493
# HO cannot be denied. There is no statistically significant difference between the control and test group purchasing averages.

#################################
# TASK 4 : Analysis of Results
#################################


df.head()
df.groupby("bidding_type").agg({"Purchase": "mean", "Earning": "mean", "Click": "mean", "Impression": "mean"})

""" 
When testing the business problem, as a result of our tests on the assumptions,
We used an independent two-sample t-test (parametric test) because the assumptions were satisfied.
According to the results we obtained, there was no significant difference between the average and maximum bidding, at a reliability rate of 95%.
In this context, together with the proposal to the customer to expand the data set and extend the duration of the tests,
In terms of clicking on the ad and generating revenue after the customer has tested on other variables,
It can be suggested that the most efficient method should be preferred.
"""


