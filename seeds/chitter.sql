DROP TABLE IF EXISTS users;
DROP SEQUENCE IF EXISTS users_id_seq;
DROP TABLE IF EXISTS posts;
DROP SEQUENCE IF EXISTS posts_id_seq;

-- Then, we recreate them
CREATE SEQUENCE IF NOT EXISTS users_id_seq;
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(255),
    user_username VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255)
);

CREATE SEQUENCE IF NOT EXISTS posts_id_seq;
CREATE TABLE posts (
    post_id SERIAL PRIMARY KEY,
    content VARCHAR(255),
    post_date timestamp,
    user_id INTEGER
);

INSERT INTO users (user_name, user_username, email, password) VALUES
('Alice', 'alice010', 'alice@alicemail.com', 'p455w0rd'),
('Bob', 'bob_test', 'bob@bobmail.com', 'bobsPass'),
('Charlie', 'cha-cha-slide', 'charlie@cmail.com', '123456');

INSERT INTO posts (content, post_date, user_id) VALUES
('Hi I''m Alice!', '2024-05-16 15:00:00', 1),
('Alright, my name is Charlie.', '2024-05-16 15:30:00', 3),
('Eyo, I am Bob.', '2024-05-16 16:00:00', 2)