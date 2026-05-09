select
  id,
  age,
  replace(nullif(sex,'NA'),' ','_') as sex,
  job as job_skill_level,
  replace(nullif(housing,'NA'),' ','_') as housing,
  replace(nullif(saving_accounts,'NA'),' ','_') as saving_accounts,
  replace(nullif(checking_account,'NA'),' ','_') as checking_account,
  credit_amount,
  duration as duration_months,
  replace(nullif(purpose,'NA'),' ','_') as purpose,
  defaulted
from {{ source('raw_applicants','raw_applicants') }}
