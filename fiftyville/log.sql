-- Keep a log of any SQL queries you execute as you solve the mystery..
-- Check all the tables in this file
.table

-- check what's inside a specific table
.schema people


-- open up crime scene report for on 7/28/2021 at Humphrey Street
SELECT description FROM crime_scene_reports WHERE month = 7 AND day = 28 AND street = 'Humphrey Street';
--| 295 | 2021 | 7     | 28  | Humphrey Street | Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery. |
--| 297 | 2021 | 7     | 28  | Humphrey Street | Littering took place at 16:36. No known witnesses.

-- open up interview ON 7/28
SELECT * FROM interviews WHERE month = 7 AND day = 28;
-- witness names: Ruth (161), Eugene (162), Raymond (163)
-- 10 minutes after theft, suspect got into a car at Emma's bakery parking lot
-- suspect made a phone call after theft
-- suspect withdraw money at ATM on Leggett St. before theft
SELECT * FROM interviews WHERE id IN (161, 162, 163);

-- check security camera
SELECT * FROM bakery_security_logs WHERE month = 7 AND day = 28;
-- suspect license plate:
--| 260 | 2021 | 7     | 28  | 10   | 16     | exit     | 5P2BI95       |
--| 264 | 2021 | 7     | 28  | 10   | 20     | exit     | G412CB7       |
--| 265 | 2021 | 7     | 28  | 10   | 21     | exit     | L93JTIZ       |
--| 266 | 2021 | 7     | 28  | 10   | 23     | exit     | 322W7JE       |
--| 267 | 2021 | 7     | 28  | 10   | 23     | exit     | 0NTHK55       |
--| 268 | 2021 | 7     | 28  | 10   | 35     | exit     | 1106N58       |

-- check people table
.schema people
-- check their infor using license plate number
SELECT * FROM people WHERE license_plate IN ('5P2BI95', 'G412CB7', 'L93JTIZ', '322W7JE', '0NTHK55', '1106N58');
--|   id   |  name   |  phone_number  | passport_number | license_plate |
--| 221103 | Vanessa | (725) 555-4692 | 2963008352      | 5P2BI95       |
--| 396669 | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       |
--| 398010 | Sofia   | (130) 555-0289 | 1695452385      | G412CB7       |
--| 449774 | Taylor  | (286) 555-6063 | 1988161715      | 1106N58       |
--| 514354 | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       |
--| 560886 | Kelsey  | (499) 555-9472 | 8294398571      | 0NTHK55       |
-- accomplice's suspect ^^
-- is this accomplice's car? did they use someone else's car?

-- check phone call log
.schema phone_calls
-- acoording to Raymond, suspect called someone as they were leaving the bakery and they talked for less than a minute.
-- suspect is caller, accomplice is receiver
-- check receiver column
SELECT * FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28
AND receiver IN ('(725) 555-4692', '(829) 555-5269', '(130) 555-0289', '(286) 555-6063', '(770) 555-1861', '(499) 555-9472');
-- | id  |     caller     |    receiver    | year | month | day | duration |
-- +-----+----------------+----------------+------+-------+-----+----------+
-- | 241 | (068) 555-0183 | (770) 555-1861 | 2021 | 7     | 28  | 371      |

-- caller: (068) 555-0183 is potential suspect. check people table with that number. get info on his name, id, passport and everything else
SELECT * FROM people WHERE phone_number = '(068) 555-0183';
-- |   id   |   name   |  phone_number  | passport_number | license_plate |
-- +--------+----------+----------------+-----------------+---------------+
-- | 231387 | Margaret | (068) 555-0183 | 1782675901      | 60563QT       |
-- margaret is potential suspect

-- check atm transactions
.schema atm_transactions
SELECT * FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street';
--| id  | account_number | year | month | day |  atm_location  | transaction_type | amount |
--+-----+----------------+------+-------+-----+----------------+------------------+--------+
--| 246 | 28500762       | 2021 | 7     | 28  | Leggett Street | withdraw         | 48     |
--| 264 | 28296815       | 2021 | 7     | 28  | Leggett Street | withdraw         | 20     |
--| 266 | 76054385       | 2021 | 7     | 28  | Leggett Street | withdraw         | 60     |
--| 267 | 49610011       | 2021 | 7     | 28  | Leggett Street | withdraw         | 50     |
--| 269 | 16153065       | 2021 | 7     | 28  | Leggett Street | withdraw         | 80     |
--| 275 | 86363979       | 2021 | 7     | 28  | Leggett Street | deposit          | 10     |
--| 288 | 25506511       | 2021 | 7     | 28  | Leggett Street | withdraw         | 20     |
--| 313 | 81061156       | 2021 | 7     | 28  | Leggett Street | withdraw         | 30     |
--| 336 | 26013199       | 2021 | 7     | 28  | Leggett Street | withdraw         | 35     |

-- check passengers table
.schema passengers
-- insert Margaret's passport number
SELECT * FROM passengers WHERE passport_number = '1782675901';
--| flight_id | passport_number | seat |
--+-----------+-----------------+------+
--| 14        | 1782675901      | 2A   |
--| 51        | 1782675901      | 4C   |

-- use passport nubmer to check passengers table
.schema passengers
SELECT * FROM passengers WHERE passport_number = 1782675901;
--| flight_id | passport_number | seat |
--+-----------+-----------------+------+
--| 14        | 1782675901      | 2A   |
--| 51        | 1782675901      | 4C   |

-- use flight id to check when did Margaret fly out
SELECT * FROM flights WHERE id IN (14, 51);
--| id | origin_airport_id | destination_airport_id | year | month | day | hour | minute |
--+----+-------------------+------------------------+------+-------+-----+------+--------+
--| 14 | 5                 | 8                      | 2021 | 7     | 26  | 12   | 8      |
--| 51 | 4                 | 8                      | 2021 | 7     | 28  | 18   | 3      |
-- check below: 4: LaGuardia, 8: Fiftyville

-- use destination airport id to check where margaret fly off to
SELECT * FROM airports;
--| id | abbreviation |                full_name                |     city      |
--+----+--------------+-----------------------------------------+---------------+
--| 1  | ORD          | O'Hare International Airport            | Chicago       |
--| 2  | PEK          | Beijing Capital International Airport   | Beijing       |
--| 3  | LAX          | Los Angeles International Airport       | Los Angeles   |
--| 4  | LGA          | LaGuardia Airport                       | New York City |
--| 5  | DFS          | Dallas/Fort Worth International Airport | Dallas        |
--| 6  | BOS          | Logan International Airport             | Boston        |
--| 7  | DXB          | Dubai International Airport             | Dubai         |
--| 8  | CSF          | Fiftyville Regional Airport             | Fiftyville    |
--| 9  | HND          | Tokyo International Airport             | Tokyo         |
--| 10 | CDG          | Charles de Gaulle Airport               | Paris         |
--| 11 | SFO          | San Francisco International Airport     | San Francisco |
--| 12 | DEL          | Indira Gandhi International Airport     | Delhi         |

--margaret's destination is fiftyville on 7/28?? it doesn't make sense

-- check bank accounts
.schema bank_accounts

-- check the earliest flight on 7/29
SELECT * FROM flights WHERE year = 2021 AND month = 7 AND day = 29;
--| id | origin_airport_id | destination_airport_id | year | month | day | hour | minute |
--| 36 | 8                 | 4                      | 2021 | 7     | 29  | 8    | 20     |
--| 43 | 8                 | 1                      | 2021 | 7     | 29  | 9    | 30     |
--earliest flight is at 8:20AM from fiftyville to LaGuardia Airport, NYC


-- check passengers on flight 36
SELECT name FROM people JOIN passengers ON people.passport_number = passengers.passport_number WHERE flight_id = 36;
--+--------+
--|  name  |
--+--------+
--| Doris  |
--| Sofia  |
--| Bruce  |
--| Edward |
--| Kelsey |
--| Taylor |
--| Kenny  |
--| Luca   |
--+--------+

-- check atm history
SELECT * FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND transaction_type = 'withdraw';
SELECT * FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND transaction_type = 'withdraw' AND atm_location LIKE 'Leggett%';
-- find out their name using their bank account number
SELECT name FROM atm_transactions JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number
JOIN people ON bank_accounts.person_id = people.id
WHERE year = 2021 AND month = 7 AND day = 28 AND transaction_type = 'withdraw' AND atm_location LIKE 'Leggett%';
--|  name   |
--+---------+
--| Bruce   |
--| Diana   |
--| Brooke  |
--| Kenny   |
--| Iman    |
--| Luca    |
--| Taylor  |
--| Benista |

-- compare with people on flight 36
--| Bruce  |
--| Taylor |
--| Kenny  |
--| Luca   |
-- Bruce, Taylor, Kenny, and Luca withdraw money from atm at Leggett St on 7/28/2021 AND took flight 36

-- check their call/phone history on 7/28/2021 after they stole the duck
SELECT * FROM people WHERE name IN ('Bruce', 'Taylor', 'Kenny', 'Luca');
SELECT * FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND caller IN (SELECT phone_number FROM people WHERE name IN ('Bruce', 'Taylor', 'Kenny', 'Luca'));
--| 233 | (367) 555-5533 | (375) 555-8161 | 2021 | 7     | 28  | 45       |
--| 236 | (367) 555-5533 | (344) 555-9601 | 2021 | 7     | 28  | 120      |
--| 245 | (367) 555-5533 | (022) 555-4052 | 2021 | 7     | 28  | 241      |
--| 254 | (286) 555-6063 | (676) 555-6554 | 2021 | 7     | 28  | 43       |
--| 279 | (826) 555-1652 | (066) 555-9701 | 2021 | 7     | 28  | 55       |
--| 284 | (286) 555-6063 | (310) 555-8568 | 2021 | 7     | 28  | 235      |
--| 285 | (367) 555-5533 | (704) 555-5790 | 2021 | 7     | 28  | 75       |
-- found Bruce, Taylor, Kenny's number in the caller list

-- filter by less than 60 seconds
--| 233 | (367) 555-5533 | (375) 555-8161 | 2021 | 7     | 28  | 45       |
--| 254 | (286) 555-6063 | (676) 555-6554 | 2021 | 7     | 28  | 43       |
--| 279 | (826) 555-1652 | (066) 555-9701 | 2021 | 7     | 28  | 55       |
-- phone_calls.id is 233, 254, 279
SELECT * FROM phone_calls WHERE id IN (233, 254, 279);

-- check bakery security logs on 7/28/2021 between 10:15 to 10:25
SELECT * FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute > 15 AND minute < 25;
-- check who is the owner of the car by using their license plate
SELECT * FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute > 15 AND minute < 25);
-- Drivers are: Vanessa, Barry, Iman, Sofia, Luca, Diana, Kelsey, Bruce
-- Bruce's car?

-- check Bruce, Kenny, Taylor's personal info again
-- who did they call after they stole the duck?
SELECT name, phone_number FROM people WHERE phone_number IN
(SELECT receiver FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND caller IN
(SELECT phone_number FROM people WHERE name IN ('Bruce', 'Taylor', 'Kenny')));
-- In phone calls id: 233 - Bruce called Robin (45s), 254 - Taylor called James (43s), 279 - Kenny called Doris (55s)

