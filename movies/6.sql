SELECT AVG(rating) FROM ratings WHERE movie_id IN (SELECT id FROM movies WHERE year = '2012');
-- query was written in 2022 around end of the year.
-- reusing the same query for the 2023 version.
