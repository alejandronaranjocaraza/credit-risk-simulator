with features as (
select
  id,

  -- Age group
  case
    when age < 30 then 'young_adult'
    when age < 45 then 'adult'
    when age < 65 then 'mature_adult'
    else 'senior' end as age_group,

  -- Age group -- numeric
  case
    when age < 30 then 0
    when age < 45 then 1
    when age < 65 then 2
    else 3 end as age_numeric_group,

  
  -- Housing stability score
  case housing
    when 'own' then 2
    when 'free' then 1
    when 'rent' then 0
  end as housing_stability_score,

  -- Skilled worker with housing stability
  case
    when job_skill_level >= 2 and housing = 'own' then 1
    else 0
  end as stable_profile_flag,

  -- Vulnerable profile: no savings, no checking info, high amount
  case
    when saving_accounts is null
     and checking_account is null
     and credit_amount > 5000 then 1
    else 0
  end as high_risk_profile_flag,
  
  -- Purpose risk groups
  case purpose
    when 'car' then 'asset_backed'
    when 'furniture/equipment' then 'asset_backed'
    when 'radio/TV' then 'consumer'
    when 'domestic appliances' then 'consumer'
    when 'business' then 'productive'
    when 'education' then 'investment'
    when 'repairs' then 'maintenance'
    else 'other'
  end as purpose_risk_group


from {{ ref('stg__german_credit') }}
)
select
  id,
  age_group,
  age_numeric_group,
  housing_stability_score,
  stable_profile_flag,
  high_risk_profile_flag,
  purpose_risk_group
from features
