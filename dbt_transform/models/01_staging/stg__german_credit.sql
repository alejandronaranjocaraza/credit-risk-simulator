select
  *
from {{ source('german_credit','raw_german_credit') }}
