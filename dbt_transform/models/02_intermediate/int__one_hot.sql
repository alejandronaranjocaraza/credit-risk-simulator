with features as (
select
  id,

  (sex = 'male')::int as is_male,
  (housing = 'own')::int as owns_home,
  (housing = 'rent')::int as rents_home,
  (purpose = 'car')::int as purpose_car,
  (purpose = 'education')::int as purpose_education

from {{ ref('stg__german_credit') }}
)
select
  id,
  is_male,
  owns_home,
  rents_home,
  purpose_car,
  purpose_education
from features
