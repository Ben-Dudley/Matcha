DROP TABLE IF EXISTS Reactions;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
  user_id SERIAL PRIMARY KEY,
  user_name TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE Reactions (
    user_id INTEGER NOT NULL ,
    target_id INTEGER CHECK ( target_id != user_id ) NOT NULL,
    reaction INTEGER NOT NULL,
    block BOOLEAN NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, target_id)
);