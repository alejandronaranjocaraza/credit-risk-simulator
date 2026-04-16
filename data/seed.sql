CREATE TABLE IF NOT EXISTS raw_german_credit (
  id SERIAL PRIMARY KEY,
  age INTEGER,
  sex VARCHAR,
  jobs INTEGER,
  housing VARCHAR,
  saving_accounts VARCHAR,
  checking_accounts VARCHAR,
  credit_amount INTEGER,
  duration INTEGER,
  purpose VARCHAR
);

COPY raw_german_credit (
  age,
  sex,
  jobs,
  housing,
  saving_accounts,
  checking_accounts,
  credit_amount,
  duration,
  purpose
)
FROM '/docker-entrypoint-initdb.d/german_credit_data.csv'
DELIMITER ','
CSV HEADER;
