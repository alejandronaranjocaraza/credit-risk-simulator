with features as (
select
  id,

  -- High amount + long duration = elevated risk
  credit_amount * duration_months as credit_exposure,

  -- Loan relative to age proxy (younger + large loan = higher risk)
  credit_amount / nullif(age, 0) as credit_per_age_year

from {{ ref('stg__german_credit') }}
)
select
  id,
  credit_exposure,
  credit_per_age_year
from features
