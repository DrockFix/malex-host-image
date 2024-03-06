create table User
(
    id         INTEGER
        primary key,
    name       TEXT not null,
    surname    TEXT not null,
    patronymic TEXT,
    sector     TEXT,
    check (sector IN ('город', 'область'))
);

