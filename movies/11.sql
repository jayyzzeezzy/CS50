SELECT title FROM movies JOIN ratings ON ratings.movie_id = movies.id JOIN stars ON stars.movie_id = movies.id JOIN people ON stars.person_id = people.id WHERE name = 'Chadwick Boseman' ORDER BY rating DESC LIMIT 5;
-- query was written in 2022 around end of the year.
-- reusing the same query for the 2023 version.
