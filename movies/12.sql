SELECT title FROM movies
JOIN stars ON stars.movie_id = movies.id
JOIN people ON people.id = stars.person_id
WHERE people.name = "Johnny Depp"
AND title IN
(SELECT title FROM movies
JOIN stars ON stars.movie_id = movies.id
JOIN people ON people.id = stars.person_id
WHERE people.name = "Helena Bonham Carter");
-- query was written in 2022 around end of the year.
-- reusing the same query for the 2023 version.
