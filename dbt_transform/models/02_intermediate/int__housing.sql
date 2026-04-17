with features as (
select
  id,

  case housing
    when 'own' then 2
    when 'free' then 1
    when 'rent' then 0
  end as housing_stability_score

from {{ ref('stg__german_credit') }}
)
select
  id,
  housing_stability_score
from features
