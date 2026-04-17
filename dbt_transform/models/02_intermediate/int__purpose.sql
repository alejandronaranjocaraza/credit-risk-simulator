with features as (
select
  id,

  case purpose
    when 'car' then 'asset_backed'
    when 'furniture/equipment' then 'asset_backed'
    when 'radio/TV' then 'consumer'
    when 'domestic appliances' then 'consumer'
    when 'business' then 'productive'
    when 'education' then 'investment'
    when 'repairs' then 'maintenance'
    else 'other'
  end as purpose_risk_group,

  -- Binary: is the loan for something tangible/asset-backed?
  (purpose in ('car', 'furniture/equipment'))::int   as is_asset_backed_loan

from {{ ref('stg__german_credit') }}
)
select
  id,
  purpose_risk_group,
  is_asset_backed_loan
from features
