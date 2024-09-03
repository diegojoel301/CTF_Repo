CREATE TABLE user (
    id INTEGER NOT NULL, 
    username VARCHAR NOT NULL, 
    password TEXT NOT NULL, 
    registration_date INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (username)
);

CREATE TABLE note (
    id INTEGER NOT NULL, 
    title VARCHAR NOT NULL, 
    content TEXT NOT NULL, 
    user_id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES user (id)
);
