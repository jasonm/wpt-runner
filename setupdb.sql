-- postgresql database setup
--
-- Run:
-- psql < setupdb.sql

DROP DATABASE IF EXISTS wptrunner_development;
CREATE DATABASE wptrunner_development WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';

\connect wptrunner_development

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE runs(uuid UUID PRIMARY KEY DEFAULT uuid_generate_v1(), data JSON);
