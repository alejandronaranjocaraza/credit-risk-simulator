with features as (
select
  id,

  -- Skilled worker with housing stability
  case
    when job_skill_level >= 2 and housing = 'own' then 1
    else 0
  end as stable_profile_flag,

  -- Vulnerable profile: no savings, no checking info, high amount
  case
    when saving_accounts is null
     and checking_accounts is null
     and credit_amount > 5000 then 1
    else 0
  end as high_risk_profile_flag

from {{ ref('stg__german_credit') }}
)
select
  id,
  stable_profile_flag,
  high_risk_profile_flag
from features
