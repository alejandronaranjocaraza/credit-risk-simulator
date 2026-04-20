select
  id,
  age,
  nullif(sex,'NA') as sex,
  job as job_skill_level,
  nullif(housing,'NA') as housing,
  nullif(saving_accounts,'NA') as saving_accounts,
  nullif(checking_account,'NA') as checking_account,
  credit_amount,
  duration as duration_months,
  nullif(purpose,'NA') as purpose,
  case
    when risk = 'good' then 1
    when risk = 'bad' then 0
    else null end as risk
from {{ source('german_credit','raw_german_credit') }}
