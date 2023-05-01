SELECT birth FROM people WHERE id = (SELECT id FROM people WHERE name = 'Emma Stone');
-- query was written in 2022 around end of the year.
-- reusing the same query for the 2023 version.
