import pandas as pd
import random

row_dic = dict()

# row = pd.DataFrame(columns=[
#    "age",
#    "sex",
#    "job",
#    "housing",
#    "saving_accounts",
#    "checking_account",
#    "credit_amount",
#    "duration",
#    "purpose"
#    ])

# Age
row_dic["age"] = random.randint(19, 80)

# Sex
row_dic["sex"] = random.choice(["male", "female"])

# Job skill level

row_dic["job"] = random.choice([0, 1, 2, 3])

# Housing
row_dic["housing"] = random.choice(["rent", "free", "own"])

# Saving account
row_dic["saving_accounts"] = random.choice([
    "quite rich",
    "moderate",
    "little",
    "rich",
    "NA"
])

# Checking account
row_dic["checking_account"] = random.choice([
    "moderate",
    "little",
    "rich",
    "NA"
])

# Credit amount (realistic distribution)
row_dic["credit_amount"] = int(random.triangular(250, 20000, 2000))

# Duration
row_dic["duration"] = int(random.triangular(4, 80, 24))

# Purpose
row_dic["purpose"] = random.choice([
    "repairs",
    "education",
    "radio/TV",
    "vacation/others",
    "business",
    "domestic appliances",
    "furniture/equipment",
    "car"
])

row = pd.DataFrame(row_dic)
