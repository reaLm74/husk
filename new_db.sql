CREATE TABLE IF NOT EXISTS tasks (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
description text NOT NULL,
done boolean DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
username text UNIQUE,
password text NOT NULL
)