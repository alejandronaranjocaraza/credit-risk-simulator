import random
from collections import defaultdict


def simulate_applications(rows=20):

    row_dict = defaultdict(list)

    for _ in range (rows):

        # Age
        age = random.randint(19, 80)
        row_dict["age"].append(age)

        # Sex
        sex = random.choice(["male", "female"])
        row_dict["sex"].append(sex)

        # Job skill level

        job = random.choice([0, 1, 2, 3])
        row_dict["job"].append(job)

        # Housing
        housing = random.choice(["rent", "free", "own"])
        row_dict["housing"].append(housing)

        # Saving account
        saving_accounts = random.choice([
            "quite rich",
            "moderate",
            "little",
            "rich",
            "NA"
        ])
        row_dict["saving_accounts"].append(saving_accounts)

        # Checking account
        checking_account = random.choice([
            "moderate",
            "little",
            "rich",
            "NA"
        ])
        row_dict["checking_account"].append(checking_account)

        # Credit amount (realistic distribution)
        credit_amount = int(random.triangular(250, 20000, 2000))
        row_dict["credit_amount"].append(credit_amount)

        # Duration
        duration = int(random.triangular(4, 80, 24))
        row_dict["duration"].append(duration)

        # Purpose
        purpose = random.choice([
            "repairs",
            "education",
            "radio/TV",
            "vacation/others",
            "business",
            "domestic appliances",
            "furniture/equipment",
            "car"
        ])
        row_dict["purpose"].append(purpose)

    return row_dict
