CREATE DATABASE trivia;
CREATE DATABASE trivia_test;
CREATE USER trivia WITH ENCRYPTED PASSWORD 'trivia';
GRANT ALL PRIVILEGES ON DATABASE trivia TO trivia;
GRANT ALL PRIVILEGES ON DATABASE trivia_test TO trivia;
ALTER USER trivia CREATEDB;
ALTER USER trivia WITH SUPERUSER;