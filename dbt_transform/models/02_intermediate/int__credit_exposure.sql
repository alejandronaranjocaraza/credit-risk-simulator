with features as (
select
  id,

  -- Log-transform skewed amount
  ln(credit_amount) as log_credit_amount,

  -- High amount + long duration = elevated risk
  credit_amount * duration_months as credit_exposure,

  -- Loan relative to age proxy (younger + large loan = higher risk)
  credit_amount / nullif(age, 0) as credit_per_age_year,
  
  -- Credit burden
  credit_amount / nullif(duration_months, 0) as monthly_payment_estimate,

  -- Duration tiers
  case
    when duration_months <= 12 then 'short'
    when duration_months <= 24 then 'medium'
    else 'long'
  end as loan_term_tier,
  
  -- Duration tiers -- numeric
  case
    when duration_months <= 12 then 0
    when duration_months <= 24 then 1
    else 3
  end as loan_term_numeric_tier

from {{ ref('stg__applicants') }}
)
select
  id,
  log_credit_amount,
  credit_exposure,
  credit_per_age_year,
  monthly_payment_estimate,
  loan_term_tier,
  loan_term_numeric_tier
from features
