CREATE TABLE books (id SERIAL PRIMARY KEY, topic TEXT, created_at TIMESTAMP, visible BOOLEAN);
CREATE TABLE messages (id SERIAL PRIMARY KEY, book_id INTEGER REFERENCES books, content TEXT);
