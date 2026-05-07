select
  id, -- primary key
  age, -- numeric
  sex, -- non-numeric
  job_skill_level, -- numeric (categorical)
  housing, -- non-numeric
  saving_accounts, -- non-numeric
  checking_account, -- non-numeric
  credit_amount, -- numeric
  duration_months, -- numeric
  purpose, -- non-numeric
  defaulted -- binary
from {{ ref('stg__applicants') }}
