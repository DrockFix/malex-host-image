create table Image
(
    id          INTEGER
        primary key,
    user_id     INTEGER not null
        references User,
    data_create DATE    not null,
    type_image  TEXT,
    path        TEXT    not null,
    avh         TEXT,
    place       TEXT,
    check (type_image IN ('шкаф', 'знак'))
);

