with features as (
select
  id,

  -- Credit burden
  credit_amount / nullif(duration_months, 0) as monthly_payment_estimate,

  -- Age buckets
  case
    when age < 25 then 'young'
    when age between 25 and 35 then 'young_adult'
    when age between 36 and 50 then 'middle_aged'
    else 'senior'
  end as age_group,

  -- Log-transform skewed amount
  ln(credit_amount) as log_credit_amount,

  -- Duration tiers
  case
    when duration_months <= 12 then 'short'
    when duration_months <= 24 then 'medium'
    else 'long'
  end as loan_term_tier

from {{ ref('stg__german_credit') }}
)
select
  id,
  monthly_payment_estimate,
  age_group,
  log_credit_amount,
  loan_term_tier
from features
