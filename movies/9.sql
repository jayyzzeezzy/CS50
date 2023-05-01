SELECT name FROM people WHERE id IN (SELECT person_id FROM stars WHERE movie_id IN (SELECT id FROM movies WHERE year = '2004')) ORDER BY birth;
-- query was written in 2022 around end of the year.
-- reusing the same query for the 2023 version.
