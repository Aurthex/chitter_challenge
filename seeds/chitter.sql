DROP TABLE IF EXISTS users;
DROP SEQUENCE IF EXISTS users_id_seq;
DROP TABLE IF EXISTS posts;
DROP SEQUENCE IF EXISTS posts_id_seq;
DROP TABLE IF EXISTS posts_users;

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

CREATE TABLE posts_users (
    post_id INTEGER,
    user_id INTEGER,
    seen boolean DEFAULT FALSE
);

INSERT INTO users (user_name, user_username, email, password) VALUES
('Alice', 'alice010', 'alice@alicemail.com', '$2b$12$fExxCJu9nlnz6ulztN1tHu.OdxGgcPkyzqqnDFWCr.CgEy0oSTHCK'),
('Bob', 'bob_test', 'bob@bobmail.com', '$2b$12$Wq4dzkBlIYNYQClPGix85eoYYAyOaVPB68FP71m9lCUtYKf.X8SF2'),
('Charlie', 'cha-cha-slide', 'charlie@cmail.com', '$2b$12$bS3rzj8S9W.sAuP1ezkNNO2Zcmr0CQIWtBegx5htKbp.deMmxPNtG');

INSERT INTO posts (content, post_date, user_id) VALUES
('Hi I''m Alice!', '2024-05-16 15:00:00', 1),
('Alright, my name is Charlie.', '2024-05-16 15:30:00', 3),
('Eyo, I am Bob.', '2024-05-16 16:00:00', 2),
('@Bob @Charlie Welcome to the site!', '2024-05-17 09:00:00', 1);

INSERT INTO posts_users (post_id, user_id) VALUES
(4,2),
(4,3);