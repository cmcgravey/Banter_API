PRAGMA foreign_keys = ON; 

CREATE TABLE Users(
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(25) NOT NULL,
    password VARCHAR(50) NOT NULL,
    banter INTEGER NOT NULL,
    fullname VARCHAR(100) NOT NULL,
    profile_picture VARCHAR(100) NOT NULL,
    UNIQUE(username)
);

CREATE TABLE Following(
    userID1 INTEGER NOT NULL,
    userID2 INTEGER NOT NULL,
    PRIMARY KEY(userID1, userID2),
    FOREIGN KEY(userID1) REFERENCES Users(userID),
    FOREIGN KEY(userID2) REFERENCES Users(userID)
);

CREATE TABLE Teams(
    teamID INTEGER PRIMARY KEY AUTOINCREMENT,
    logo VARCHAR(100) NOT NULL,
    name VARCHAR(50) NOT NULL,
    abbr VARCHAR(10) NOT NULL
);

CREATE TABLE Games(
    gameID INTEGER PRIMARY KEY AUTOINCREMENT,
    fixtureID INTEGER NOT NULL,
    league VARCHAR(50) NOT NULL,
    teamID1 INTEGER NOT NULL,
    teamID2 INTEGER NOT NULL,
    team1_score INTEGER NOT NULL,
    team2_score INTEGER NOT NULL,
    time_elapsed VARCHAR(20) NOT NULL,
    status VARCHAR(15) NOT NULL,
    num_questions INTEGER NOT NULL,
    start_time VARCHAR(100) NOT NULL,
    UNIQUE(fixtureID),
    FOREIGN KEY(teamID1) REFERENCES Teams(teamID), 
    FOREIGN KEY(teamID2) REFERENCES Teams(teamID)
);

CREATE TABLE Questions(
    questionID INTEGER PRIMARY KEY AUTOINCREMENT,
    gameID INTEGER NOT NULL,
    locked VARCHAR(10) NOT NULL,
    text VARCHAR(100) NOT NULL,
    label VARCHAR(100) NOT NULL,
    question_stage VARCHAR(100) NOT NULL,
    opt1 VARCHAR(50) NOT NULL,
    worth1 INTEGER NOT NULL,
    decrease1 INTEGER NOT NULL,
    opt2 VARCHAR(50) NOT NULL,
    worth2 INTEGER NOT NULL,
    decrease2 INTEGER NOT NULL,
    opt3 VARCHAR(50) NOT NULL,
    worth3 INTEGER NOT NULL,
    decrease3 INTEGER NOT NULL,
    answer VARCHAR(50) NOT NULL,
    type VARCHAR(50) NOT NULL,
    tag VARCHAR(50) NOT NULL,
    FOREIGN KEY(gameID) REFERENCES Games(gameID)
);

CREATE TABLE Answers(
    userID INTEGER NOT NULL,
    questionID INTEGER NOT NULL,
    answer VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY(userID) REFERENCES Users(userID),
    FOREIGN KEY(questionID) REFERENCES Questions(questionID),
    PRIMARY KEY(userID, questionID)
);

CREATE TABLE ScoreWith(
    teamID INTEGER NOT NULL,
    userID INTEGER NOT NULL,
    score INTEGER NOT NULL,
    PRIMARY KEY(userID, teamID),
    FOREIGN KEY(teamID) REFERENCES Teams(teamID),
    FOREIGN KEY(userID) REFERENCES Users(userID)
);