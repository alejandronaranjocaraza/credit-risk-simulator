with cte as (
select
  id,

  -- Ordinal encoding for savings risk level
  case saving_accounts
    when 'little' then 1
    when 'moderate' then 2
    when 'quite_rich' then 3
    when 'rich' then 4
    else 0-- unknown/NA treated as worst case
  end as savings_score,

  -- Same for checking
  case checking_accounts
    when 'little' then 1
    when 'moderate' then 2
    when 'rich' then 3
    else 0
  end as checking_score,
  
  -- Binary flags
  (saving_accounts is null)::int as has_no_savings_info,
  (checking_accounts is null)::int as has_no_checking_info

from {{ ref('stg__german_credit') }}
),
features as (
select

  id,
  savings_score,
  checking_score,
  has_no_savings_info,
  has_no_checking_info,

  -- Combined liquidity score
  (savings_score + checking_score) as total_liquidity_score

from cte
)
select
  id,
  savings_score,
  checking_score,
  total_liquidity_score,
  has_no_savings_info,
  has_no_checking_info
from features
