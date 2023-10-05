PRAGMA foreign_keys = ON; 

CREATE TABLE Users(
    userID INTEGER NOT NULL,
    username VARCHAR(25) NOT NULL,
    password VARCHAR(50) NOT NULL,
    banter INTEGER NOT NULL,
    PRIMARY KEY(userID)
);

CREATE TABLE Teams(
    teamID INTEGER NOT NULL,
    logo VARCHAR(100) NOT NULL,
    name VARCHAR(50) NOT NULL,
    PRIMARY KEY(teamID)
);

CREATE TABLE Games(
    gameID INTEGER NOT NULL,
    teamID1 INTEGER NOT NULL,
    teamID2 INTEGER NOT NULL,
    status VARCHAR(15) NOT NULL,
    num_questions INTEGER NOT NULL,
    PRIMARY KEY(gameID),
    FOREIGN KEY(teamID1) REFERENCES Teams(teamID), 
    FOREIGN KEY(teamID2) REFERENCES Teams(teamID)
);

CREATE TABLE Questions(
    questionID INTEGER NOT NULL,
    gameID INTEGER NOT NULL,
    worth INTEGER NOT NULL,
    PRIMARY KEY(questionID),
    FOREIGN KEY(gameID) REFERENCES Games(gameID)
);

CREATE TABLE Answers(
    userID INTEGER NOT NULL,
    questionID INTEGER NOT NULL,
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