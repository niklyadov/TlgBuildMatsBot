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

create trigger check_on_user_update
    before update on users
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
    -- может быть очень ресурсозатратно ----------------------------
    select raise(abort, 'User does not exist.')                   --
        where new.user_id not in (select telegram_id from users); --
    ----------------------------------------------------------------
    select raise(abort, 'Top count must be greater than 0 and lesser or equal than 10.')
        where new.top_count <= 0 or new.top_count > 10;
    select raise(abort, 'Ordering does not exist.')
        where new.ordering_id not in (select id from ordering);
end;

-- Requests ------------------------------------------------------------------------------------------------------------

create table Requests (
    id integer primary key,
    date text,
    full_name text not null,
    key_word_id integer not null,
    result text not null,
    foreign key (key_word_id) references key_words(id)
);

create trigger error_on_request_update
    before update on settings
begin
    select raise(abort, 'You cannot update requests.');
end;

create trigger set_datetime_now_on_request_insert
    after insert on requests
begin
    delete from requests where id = new.id;
    insert
        into requests (id, date, result)
        values
        (
            new.id,
            strftime('%Y-%m-%d %H:%M:%S', datetime('now')),
            new.result
        );
end;

create trigger renew_favourites_on_request_insert
    after insert on requests
    when new.full_name in
         (select
            r.full_name
         from logs l
         join requests r
            on l.request_id = r.id
         where l.id in (select f.log_id from favourites f))
begin
    insert into Renewed_Favourites (user_id, full_name)
    values (select l.user_id
            from logs l
            where l.request_id in (
                select r.id
                from requests r
                where r.full_name = new.full_name))),
            new.full_name)
end;

-- Key_Words -----------------------------------------------------------------------------------------------------------

create table Key_Words (
    id integer primary key,
    word text not null
);
-- create some keywords --

-- Favourites ----------------------------------------------------------------------------------------------------------

create table Favourites (
    id integer primary key,
    log_id integer not null,
    foreign key (log_id) references requests(id)
);

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
    request_id integer not null,
    message_id integer not null,
    foreign key (user_id) references users(telegram_id),
    foreign key (request_id) references Requests(id),
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
    full_name text not null,
    foreign key (user_id) references Users(telegram_id),
)