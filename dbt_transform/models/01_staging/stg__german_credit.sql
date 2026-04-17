select
  id,
  age,
  nullif(sex,'NA') as sex,
  jobs as job_skill_level,
  nullif(housing,'NA') as housing,
  nullif(saving_accounts,'NA') as saving_accounts,
  nullif(checking_accounts,'NA') as checking_accounts,
  credit_amount,
  duration as duration_months,
  nullif(purpose,'NA') as purpose
from {{ source('german_credit','raw_german_credit') }}
