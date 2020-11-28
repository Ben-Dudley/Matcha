DROP TABLE IF EXISTS UserInterestRelation;
DROP TABLE IF EXISTS Interests;
DROP TABLE IF EXISTS Reactions;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
  user_id SERIAL PRIMARY KEY,
  user_name TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT NOT NULL,
  gender BOOLEAN,
  preference BOOLEAN,
  biography TEXT
);

CREATE TABLE Reactions (
    user_id INTEGER NOT NULL,
    target_id INTEGER CHECK ( target_id != user_id ) NOT NULL,
    reaction INTEGER NOT NULL,
    block BOOLEAN NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_target FOREIGN KEY(target_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, target_id)
);

CREATE TABLE Interests (
    interest_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE UserInterestRelation (
    user_id INTEGER NOT NULL,
    interest_id INTEGER NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, interest_id)
)