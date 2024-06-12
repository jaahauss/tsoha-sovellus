CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, admin BOOLEAN);
CREATE TABLE books (id SERIAL PRIMARY KEY, topic TEXT, created_at TIMESTAMP, visible BOOLEAN);
CREATE TABLE messages (id SERIAL PRIMARY KEY, book_id INTEGER REFERENCES books, content TEXT, user_id INTEGER REFERENCES users, visible BOOLEAN);
CREATE TABLE suggestions (id SERIAL PRIMARY KEY, content TEXT, visible BOOLEAN);
CREATE TABLE reviews (id SERIAL PRIMARY KEY, grade INTEGER, book_id INTEGER REFERENCES books);

