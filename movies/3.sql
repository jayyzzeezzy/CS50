SELECT title FROM movies WHERE id IN (SELECT id FROM movies WHERE year >= '2018') ORDER BY title;
-- query was written in 2022 around end of the year.
-- reusing the same query for the 2023 version.
