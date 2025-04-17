CREATE TABLE IF NOT EXISTS Users (
    userId SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    passwordHash BYTEA NOT NULL,
    createdAt TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Profiles (
    userId SERIAL PRIMARY KEY REFERENCES Users,
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    birthdate DATE,
    email VARCHAR(50) UNIQUE,
    phoneNumber VARCHAR(20) UNIQUE
);

CREATE TABLE IF NOT EXISTS Sessions (
    sessionId SERIAL PRIMARY KEY,
    userId SERIAL REFERENCES Users,
    token VARCHAR(300),
    createdAt TIMESTAMP DEFAULT NOW(),
    expiresAt TIMESTAMP
);
