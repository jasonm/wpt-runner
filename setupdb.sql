-- postgresql database setup
--
-- Run:
-- psql < setupdb.sql

DROP DATABASE IF EXISTS wptrunner_development;
CREATE DATABASE wptrunner_development WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';

\connect wptrunner_development

CREATE TABLE tests(id SERIAL PRIMARY KEY, server VARCHAR(255), label VARCHAR(255), test_id VARCHAR(255), status VARCHAR(255));
CREATE TABLE results(id SERIAL PRIMARY KEY, data JSON);
