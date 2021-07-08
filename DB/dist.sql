-- Roles ---------------------------------------------------------------------------------------------------------------

create table Roles (
    id integer primary key,
    name text not null
);
insert into Roles (name) values ('super_user');
insert into Roles (name) values ('admin');
insert into Roles (name) values ('default_user');

-- Users ---------------------------------------------------------------------------------------------------------------

create table Users (
    telegram_id integer primary key,
    role_id integer not null,
    start_date text,
    foreign key (role_id) references roles(id)
);

create trigger check_on_user_insert
    before insert on users
begin
    select raise(abort, 'Role does not exist.')
        where new.role_id not in (select id from roles);
end;

create trigger create_default_settings_on_user_insert
    after insert on users
begin
    insert
        into settings (user_id, top_count, ordering_id)
        values
        (
            new.telegram_id,
            3,
            (select id from ordering where name = 'cost')
        );
end;

create trigger set_datetime_now_on_user_insert
    after insert on users
begin
    update users
        set start_date = strftime('%Y-%m-%d %H:%M:%S', datetime('now')) where telegram_id = new.telegram_id;
end;

-- Ordering ------------------------------------------------------------------------------------------------------------

create table Ordering (
    id integer primary key,
    name text not null
);
insert into ordering (name) values ('cost');
insert into ordering (name) values ('rating');
insert into ordering (name) values ('naming');
insert into ordering (name) values ('naming_reversed');

-- Settings ------------------------------------------------------------------------------------------------------------

create table Settings (
    user_id integer primary key,
    top_count integer not null,
    ordering_id integer not null,
    foreign key (user_id) references users(telegram_id),
    foreign key (ordering_id) references ordering(id)
);

create trigger error_on_settings_insert
    before insert on settings
    when new.top_count <> 3
        or new.ordering_id <> (select id from ordering where name = 'cost')
begin
    select raise(abort, 'You cannot insert settings.');
end;

create trigger check_on_settings_update
    before update on settings
begin
    select raise(abort, 'Top count must be greater than 0 and lesser than 10.')
        where new.top_count <= 0 or new.top_count > 9;
    select raise(abort, 'Ordering does not exist.')
        where new.ordering_id not in (select id from ordering);
end;

-- Requests ------------------------------------------------------------------------------------------------------------

create table Requests (
    id integer primary key,
    date text,
    full_name text not null,
    price text not null,
    key_word_id integer not null,
    result text not null,
    foreign key (key_word_id) references key_words(id)
);

create trigger error_on_request_update
    before update on Requests
begin
    select raise(abort, 'You cannot update requests.');
end;

create trigger set_datetime_now_on_request_insert
    after insert on requests
begin
    delete from requests where id = new.id;
    insert
        into requests (id, full_name, price, key_word_id, date, result)
        values
        (
            new.id,
            new.full_name,
            new.price,
            new.key_word_id,
            strftime('%Y-%m-%d %H:%M:%S', datetime('now')),
            new.result
        );
end;

create trigger renew_favourites_on_request_insert
    after insert on requests
    when ((select count() from (select result from logs
         where id in (select log_id from favourites) and lower(Logs.result) like '%'||lower(new.full_name)||'%')) > 0)
begin
    insert into Renewed_Favourites (user_id, old_price, new_price, full_name)
    values ((select user_id
                from logs
                where lower(result) like '%'||lower(new.full_name)||'%'),
            (select price
                from logs
                where lower(result) like '%'||lower(new.full_name)||'%'),
            new.price,
            new.full_name);
end;

-- Key_Words -----------------------------------------------------------------------------------------------------------

create table Key_Words (
    id integer primary key,
    word text not null
);

insert into Key_Words (word) values ('шпатлевка');
insert into Key_Words (word) values ('краска');
insert into Key_Words (word) values ('цемент');
insert into Key_Words (word) values ('профиль');
insert into Key_Words (word) values ('гипсокартон');
insert into Key_Words (word) values ('обои');
insert into Key_Words (word) values ('пена монтажная');
insert into Key_Words (word) values ('утеплитель');
insert into Key_Words (word) values ('саморез');
insert into Key_Words (word) values ('гвоздь');
insert into Key_Words (word) values ('шуруп');
insert into Key_Words (word) values ('болт');
insert into Key_Words (word) values ('штукатурка');
insert into Key_Words (word) values ('клей для плитки');
insert into Key_Words (word) values ('фанера');
insert into Key_Words (word) values ('дсп');
insert into Key_Words (word) values ('двп');
insert into Key_Words (word) values ('цсп');
insert into Key_Words (word) values ('гсп');
insert into Key_Words (word) values ('арматура');
insert into Key_Words (word) values ('швеллер');
insert into Key_Words (word) values ('грунтовка');
insert into Key_Words (word) values ('доска');
insert into Key_Words (word) values ('вагонка');
insert into Key_Words (word) values ('брус');
insert into Key_Words (word) values ('жидкие гвозди');
insert into Key_Words (word) values ('гипс');
insert into Key_Words (word) values ('щебень');
insert into Key_Words (word) values ('песок');
insert into Key_Words (word) values ('облицовочный кирпич');
insert into Key_Words (word) values ('строительный кирпич');
insert into Key_Words (word) values ('гидроизоляция');
insert into Key_Words (word) values ('шлакоблок');
insert into Key_Words (word) values ('камень');
insert into Key_Words (word) values ('бетон');

-- Favourites ----------------------------------------------------------------------------------------------------------

create table Favourites (
    id integer primary key,
    log_id integer not null,
    foreign key (log_id) references logs(id)
);

create trigger check_logs_on_favourite_insert
    before insert on Favourites
    when new.log_id in (select log_id from Favourites)
begin
    select raise(abort, 'You cannot insert log that already exists into favourites.');
end;

-- Messages ------------------------------------------------------------------------------------------------------------

create table Messages (
    id integer primary key,
    message text not null
);
insert into messages (message) values ('error');
insert into messages (message) values ('partially_done');
insert into messages (message) values ('successful');

-- Logs ----------------------------------------------------------------------------------------------------------------

create table Logs (
    id integer primary key,
    date text,
    search_word integer not null,
    user_id integer not null,
    price real not null,
    result text not null,
    message_id integer not null,
    foreign key (user_id) references users(telegram_id),
    foreign key (message_id) references messages(id)
);

create trigger check_on_logs_insert
    before insert on logs
begin
    select raise(abort, 'Message does not exist.')
        where new.message_id not in (select id from messages);
end;

create trigger check_on_logs_update
    before update on logs
begin
    select raise(abort, 'Message does not exist.')
        where new.message_id not in (select id from messages);
end;

create trigger set_datetime_now_on_log_insert
    after insert on logs
begin
    update logs
        set date = strftime('%Y-%m-%d %H:%M:%S', datetime('now')) where id = new.id;
end;

-- Renewed_Favourites --------------------------------------------------------------------------------------------------

create table Renewed_Favourites (
    id integer primary key,
    user_id integer not null,
    old_price real not null,
    new_price real not null,
    full_name text not null,
    foreign key (user_id) references Users(telegram_id)
)