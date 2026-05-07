CREATE TABLE IF NOT EXISTS raw_applicants (
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
  simulated_at TIMESTAMP DEFAULT NOW(),
  rating DECIMAL DEFAULT NULL,
  approved BOOLEAN DEFAULT NULL,
  defaulted BOOLEAN DEFAULT NULL
);

COPY raw_applicants (
  age,
  sex,
  job,
  housing,
  saving_accounts,
  checking_account,
  credit_amount,
  duration,
  purpose,
  defaulted
)
FROM '/docker-entrypoint-initdb.d/german_credit_data.csv'
DELIMITER ','
CSV HEADER;
