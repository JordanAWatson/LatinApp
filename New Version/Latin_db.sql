CREATE SCHEMA `latin_verbs` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
USE latin_verbs;

CREATE TABLE dictionary (
	verb 		VARCHAR(28),
    conjugation	CHAR(3),			/* 1st, 2nd, 3rd, 4th, 3io, IRG */
    PRIMARY KEY (verb)
);

CREATE TABLE verbForm (
	form 	VARCHAR(28),			/* The conjugated verb form */
    stem 	VARCHAR(28),			/* Its first principle part */
    PRIMARY KEY (form),
    FOREIGN KEY (stem) REFERENCES dictionary(verb)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE formInfo (
	form 	VARCHAR(28),
	voice 	CHAR(3),				/* ACT, PAS */
    mood 	CHAR(3), 				/* IND, SUB, IMP, INF */
    tense 	CHAR(4),				/* PRES, IMPF, FUTR, PERF, PLPF, FRPF */
    number 	TINYINT UNSIGNED,	/* 1, 2 */
    person 	TINYINT UNSIGNED,	/* 1, 2, 3 */
    FOREIGN KEY (form) REFERENCES verbForm(form)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);


CREATE SCHEMA `latin_nouns` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
USE latin_nouns;

CREATE TABLE noun (
	noms	varchar(28),
    gens	varchar(28),
    dats	varchar(28),
    accs	varchar(28),
    vocs	varchar(28),
    locs	varchar(28),
    nomp	varchar(28),
    genp	varchar(28),
    datp	varchar(28),
    accp	varchar(28),
    ablp	varchar(28),
    vocp	varchar(28),
    locp	varchar(28),
    translation	varchar(28),
    declension	varchar(28),
    gender		varchar(28)
);