select
  -- Primary key
  bf.id,

  -- Target
  bf.risk,

  -- General profile
  bf.age,
  p.age_numeric_group,
  p.age_group, -- non-numeric
  bf.sex, -- non-numeric

  -- Credit exposure
  bf.duration_months,
  bf.credit_amount,
  ce.log_credit_amount,
  ce.credit_exposure,
  ce.credit_per_age_year,
  ce.monthly_payment_estimate,
  ce.loan_term_numeric_tier,
  ce.loan_term_tier, -- non-numeric

  -- Liquidity
  l.savings_score,
  l.checking_score,
  l.total_liquidity_score,
  l.has_no_savings_info,
  l.has_no_checking_info,
  bf.saving_accounts, -- non-numeric
  bf.checking_account, -- non-numeric

  -- Profile risk
  bf.job_skill_level,
  p.housing_stability_score,
  p.stable_profile_flag,
  p.high_risk_profile_flag,
  bf.housing, -- non numeric
  bf.purpose, -- non numeric
  p.purpose_risk_group -- non numeric
  
from {{ ref('int__base_features') }} bf
left join {{ ref('int__credit_exposure') }} ce using (id)
left join {{ ref('int__liquidity') }} l using (id)
left join {{ ref('int__profile') }} p using (id)
