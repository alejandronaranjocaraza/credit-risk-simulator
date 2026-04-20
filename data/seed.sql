CREATE TABLE IF NOT EXISTS raw_german_credit (
  id SERIAL PRIMARY KEY,
  age INTEGER,
  sex VARCHAR,
  job INTEGER,
  housing VARCHAR,
  saving_accounts VARCHAR,
  checking_account VARCHAR,
  credit_amount INTEGER,
  duration INTEGER,
  purpose VARCHAR,
  risk VARCHAR
);

COPY raw_german_credit (
  age,
  sex,
  job,
  housing,
  saving_accounts,
  checking_account,
  credit_amount,
  duration,
  purpose,
  risk
)
FROM '/docker-entrypoint-initdb.d/german_credit_data.csv'
DELIMITER ','
CSV HEADER;
