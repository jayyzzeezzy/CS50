SELECT name FROM people WHERE id IN (SELECT person_id FROM directors WHERE movie_id IN (SELECT movie_id FROM ratings WHERE rating >= 9.0));
-- query was written in 2022 around end of the year.
-- reusing the same query for the 2023 version.
