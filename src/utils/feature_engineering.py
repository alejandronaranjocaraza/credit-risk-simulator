import math
import pandas as pd


def stage_applicant(data: dict) -> dict:
    # mirrors stg__applicants.sql

    return {
        "age": data["age"],
        "sex": None if data.get("sex") == "NA" else data.get("sex"),
        "job_skill_level": data["job"],
        "housing": None if data.get("housing") == "NA" else data.get("housing"),
        "saving_accounts": None if data.get("saving_accounts") == "NA" else data.get("saving_accounts"),
        "checking_account": None if data.get("checking_account") == "NA" else data.get("checking_account"),
        "credit_amount": data["credit_amount"],
        "duration_months": data["duration"],
        "purpose": None if data.get("purpose") == "NA" else data.get("purpose"),
    }


def add_credit_exposure(data: dict) -> dict:
    # mirrors int__credit_exposure.sql
    credit_amount = data["credit_amount"]
    duration_months = data["duration_months"]
    age = data["age"]

    data["log_credit_amount"] = math.log(credit_amount) if credit_amount > 0 else None
    data["credit_exposure"] = credit_amount * duration_months
    data["credit_per_age_year"] = credit_amount / age if age else None
    data["monthly_payment_estimate"] = credit_amount / duration_months if duration_months else None

    if duration_months <= 12:
        data["loan_term_tier"] = "short"
        data["loan_term_numeric_tier"] = 0
    elif duration_months <= 24:
        data["loan_term_tier"] = "medium"
        data["loan_term_numeric_tier"] = 1
    else:
        data["loan_term_tier"] = "long"
        data["loan_term_numeric_tier"] = 3

    return data


def add_liquidity(data: dict) -> dict:
    # mirrors int__liquidity.sql

    savings_map = {"little": 1, "moderate": 2, "quite_rich": 3, "rich": 4}
    checking_map = {"little": 1, "moderate": 2, "rich": 3}

    savings = data.get("saving_accounts")
    checking = data.get("checking_account")

    data["savings_score"] = savings_map.get(savings, 0)
    data["checking_score"] = checking_map.get(checking, 0)
    data["has_no_savings_info"] = 1 if savings is None else 0
    data["has_no_checking_info"] = 1 if checking is None else 0
    data["total_liquidity_score"] = data["savings_score"] + data["checking_score"]

    return data


def add_profile(data: dict) -> dict:
    # mirrors int__profile.sql

    age = data["age"]
    housing = data.get("housing")
    purpose = data.get("purpose")
    job_skill_level = data["job_skill_level"]
    saving_accounts = data.get("saving_accounts")
    checking_account = data.get("checking_account")
    credit_amount = data["credit_amount"]

    if age < 30:
        data["age_group"] = "young_adult"
        data["age_numeric_group"] = 0
    elif age < 45:
        data["age_group"] = "adult"
        data["age_numeric_group"] = 1
    elif age < 65:
        data["age_group"] = "mature_adult"
        data["age_numeric_group"] = 2
    else:
        data["age_group"] = "senior"
        data["age_numeric_group"] = 3

    # housing stability
    housing_map = {"own": 2, "free": 1, "rent": 0}
    data["housing_stability_score"] = housing_map.get(housing, 0)

    # stable profile flag
    data["stable_profile_flag"] = 1 if (job_skill_level >= 2 and housing == "own") else 0

    # high risk profile flag
    data["high_risk_profile_flag"] = 1 if (
        saving_accounts is None and
        checking_account is None and
        credit_amount > 5000
    ) else 0

    # purpose risk group
    purpose_map = {
        "car": "asset_backed",
        "furniture/equipment": "asset_backed",
        "radio/TV": "consumer",
        "domestic appliances": "consumer",
        "business": "productive",
        "education": "investment",
        "repairs": "maintenance",
    }
    data["purpose_risk_group"] = purpose_map.get(purpose, "other")

    return data


def build_features(raw_input: dict) -> pd.DataFrame:
    # Full pipeline — takes raw applicant dict, returns a single-row DataFrame
    # ready for model prediction. Mirrors the full dbt pipeline.
    
    data = stage_applicant(raw_input)
    data = add_credit_exposure(data)
    data = add_liquidity(data)
    data = add_profile(data)
    return pd.DataFrame([data])
