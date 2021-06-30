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
    user_id integer not null,
    date text not null,
    result text not null,
    foreign key (user_id) references users(telegram_id)
);

-- может быть очень ресурсозатратно --------------------------------
create trigger check_on_request_insert                            --
    before insert on settings                                     --
begin                                                             --
    select raise(abort, 'User does not exist.')                   --
        where new.user_id not in (select telegram_id from users); --
end;                                                              --
--------------------------------------------------------------------

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
        into requests (id, user_id, date, result)
        values
        (
            new.id,
            new.user_id,
            strftime('%Y-%m-%d %H:%M:%S', datetime('now')),
            new.result
        );
end;

create trigger log_on_request_insert
    after insert on requests
begin
    insert
        into logs (request_id, message_id)
        values
        (
            new.id,
            (select id from messages
                where message = (case when rowid = -1 then 'error' else 'successful' end))
        );
end;

-- Favourites ----------------------------------------------------------------------------------------------------------

create table Favourites (
    id integer primary key,
    request_id integer not null,
    foreign key (request_id) references requests(id)
);

-- может быть очень ресурсозатратно -----------------------------
create trigger check_on_favourites_insert                      --
    before insert on favourites                                --
begin                                                          --
    select raise(abort, 'Role does not exist.')                --
        where new.request_id not in (select id from requests); --
end;                                                           --
                                                               --
create trigger check_on_favourites_update                      --
    before update on favourites                                --
begin                                                          --
    select raise(abort, 'Role does not exist.')                --
        where new.request_id not in (select id from requests); --
end;                                                           --
-----------------------------------------------------------------

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
    request_id integer not null,
    message_id integer not null,
    foreign key (request_id) references requests(id),
    foreign key (message_id) references messages(id)
);


create trigger check_on_logs_insert
    before insert on logs
begin
    -- может быть очень ресурсозатратно -------------------------
    select raise(abort, 'Role does not exist.')                --
        where new.request_id not in (select id from requests); --
    -------------------------------------------------------------
    select raise(abort, 'Message does not exist.')
        where new.message_id not in (select id from messages);
end;

create trigger check_on_logs_update
    before update on logs
begin
    -- может быть очень ресурсозатратно -------------------------
    select raise(abort, 'Role does not exist.')                --
        where new.request_id not in (select id from requests); --
    -------------------------------------------------------------
    select raise(abort, 'Message does not exist.')
        where new.message_id not in (select id from messages);
end;

-- Categories ----------------------------------------------------------------------------------------------------------

create table Categories (
    id integer primary key,
    name text not null
);
insert into categories (name) values ('insulation');
insert into categories (name) values ('waterproofing');
insert into categories (name) values ('primers');
insert into categories (name) values ('membranes');
insert into categories (name) values ('bricks');
insert into categories (name) values ('cement');
insert into categories (name) values ('building blocks');

-- Price_History -------------------------------------------------------------------------------------------------------

create table Price_History (
    id integer primary key,
    category_id integer not null,
    date text,
    price real,
    foreign key (category_id) references categories(id)
);

create trigger check_on_price_history_insert
    before insert on price_history
begin
    select raise(abort, 'Category does not exist.')
        where new.category_id not in (select id from categories);
end;

create trigger check_on_price_history_update
    before update on price_history
begin
    select raise(abort, 'Category does not exist.')
        where new.category_id not in (select id from categories);
end;

create trigger set_datetime_now_on_price_history_insert
    after insert on requests
begin
    update requests
        set date = strftime('%Y-%m-%d %H:%M:%S', datetime('now')) where id = new.id;
end;