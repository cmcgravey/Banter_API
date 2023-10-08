# Banter API Documentation

By: Colin McGravey

## Section 1: Scripts 

###### bin/run_db (create | destroy | reset | dump)

The db script can be run from the command line and must be run with one keyword argument (create, destroy, reset, or dump). Running the script with 'dump' specified will dump all tables of the database into output. Create, destroy, reset, all deal with tearing down the database or initializing. 

###### bin/run_api

This script takes no keyword arguments, and simply runs the flask application on your local machine on port 8000. 

###### bin/test_api

This script also takes no keyword arguments and runs through a mock use case of the API, inserting users, questions, answers, and updating user scores. 


## Section 2: Basic Request Syntax 
All requests should be made with a JSON body. Inside the JSON, for every request made, include the private API key in a field titled "api_key". Each request will demand for different fields to be included and will be explained later in this document. The only route that can be accessed with no API key is http://localhost:8000/api/routes/, which displays the possible API endpoints. 

This documentation is written assuming the API is running on your local machine, however, if it is in some deployed environment, the request URLs should be changed accordingly. 


###### Example: JSON body for request

```
{
    "api_key": "xxxxxxxxxxx",
    "username": "cmcgravey",
    "password": "password"
}
```

## Section 3: Routes Endpoint

###### http://localhost:8000/api/routes/

Request body is unneccessary for this route as it does not require an API key, nor any extraneous information. Response will be in the form ...

```
{
    "routes": "GET /api/routes/",
    "users": [
        {"insert_user": "POST /api/users/"},
        {"fetch_user": "GET /api/users/<user_id_slug>/"},
        {"update_user": "POST /api/users/<user_id_slug>/"},
        {"logon_user": "POST /api/users/logon/"}
    ],
    "teams": [
        {"insert_team": "POST /api/teams/"}, 
        {"fetch_team": "GET /api/teams"}
    ],
    "games": [
        {"insert_game": "POST /api/games/"},
        {"update_game": "POST /api/games/<game_id_slug>/"},
        {"fetch_one": "GET /api/games/<game_id_slug>/"},
        {"fetch_multiple": "GET /api/games/"}
    ], 
    "answers": [
        {"insert_answer": "POST /api/answers/<question_id_slug>/"}
    ],
    "questions": [
        {"insert_question": "POST /api/questions/<game_id_slug>/"},
        {"update_question_answer": "POST /api/questions/update/<question_id_slug>/"},
        {"fetch_game_questions": "GET /api/questions/<game_id_slug>/"}
    ]
}
```

**The remainder of the documentation will touch on each of the other five endpoints.** 

## Section 4: Users Routes

###### **POST /api/users/**

This route will insert a user into the database. 

*Input* 
```
{
    "api_key": "xxxxxxxxxxx",
    "username": "cmcgravey", 
    "password": "password" 
}
```

*Output* 
```
{
    "userID": 1,
    "username": "cmcgravey",
    "banter": 0
}
```

###### **POST /api/users/<user_id_slug>/**

Updates a user's password or score

*Input* 
```
{
    "api_key": "xxxxxxxx",
    "type": "password" || "banter",
    "new_banter": 45,
    "new_password": "password"
}
```
*Output* 
```
{
    "userID": 1,
    "username": "cmcgravey",
    "banter": 0
}
```

If the route is being utilized for a password update, do not include the field "new_banter". The same is true for if you are updating banter score, do not include the field "new_password".

###### **POST /api/users/logon/**

Route simulates logging on a user, receives a username and password and determines if the information is valid. 

*Input* 
```
{
    "api_key": "xxxxxxxxx",
    "username": "cmcgravey",
    "password": "password"
}
```
*Output #1* 
```
{
    "userID": 1,
    "username": "cmcgravey",
    "banter": 0
}
```
*Output #2* 
```
{
    "msg": "Invalid Password"
}
```
*Output #3* 
```
{
    "msg": "Invalid User"
}
```

Outputs 2 and 3 result from invalid user information being given to the API. 

###### **GET /api/users/<user_id_slug>/**

Route fetches the information for one user by userID. 

*Input* 
```
{
    "api_key": "xxxxxxxxx"
}
```
*Output* 
```
{
    "userID": 1,
    "username": "cmcgravey",
    "banter": 0
}
```

## Section 5: Teams Routes

###### **POST /api/teams/**

Inserts a team into the database.

*Input* 
```
{
    "api_key": "xxxxxxxx",
    "name": "Chelsea", 
    "abbr": "CHE",
    "logo": "chelsea.png"
}
```
*Output* 
```
{
    "teamID": 1,
    "name": "Chelsea"
}
```

###### **GET /api/teams/<team_id_slug>/**

Fetches team from the database according to teamID. 

*Input* 
```
{
    "api_key": "xxxxxxxx"
}
```
*Output* 
```
{
    "name": "Chelsea",
    "abbr": "CHE",
    "logo": "chelsea.png",
    "teamID": 1
}
```

## Section 6: Games Routes

###### **POST /api/games/**

Inserts a game into the database.

*Input* 
```
{
    "api_key": "xxxxxxxxx",
    "teamID1": 1,
    "teamID2": 2
}
```
*Output* 
```
{
    "gameID": 1,
    "teamID1": 1,
    "teamID2": 2
}
```

###### **POST /api/games/<game_id_slug>/**

Updates the status of a game. Game statuses can be one of three values in the database, 'PENDING', 'IN PLAY', or 'COMPLETE'.

*Input* 
```
{
    "api_key": "xxxxxxxxxx",
    "update": "IN PLAY"
}
```
*Output* 
```
{
    "gameID": 1,
    "team1": 1,
    "team2": 2,
    "status": "IN PLAY",
    "num_questions": 0
}
```

Updates to the num_questions field are not performed by this route. Instead, num_questions is updated automatically as a question is inserted to the database pertaining to a particular gameID. 

###### **GET /api/games/<game_id_slug>/**

Fetches one game by gameID. 

*Input* 
```
{
    "api_key": "xxxxxxxxx"
}
```
*Output*
```
{
    "gameID": 1,
    "team1": 1,
    "team2": 2,
    "status": "IN PLAY",
    "num_questions": 0
}
```

###### **GET /api/games/**

Fetches all games of a particular status, i.e. 'PENDING', 'IN PLAY', 'COMPLETED'

*Input* 
```
{
    "api_key": "xxxxxxxxxx",
    "status": "IN PLAY"
}
```
*Output* 
```
{
    "games": [
        {
            "gameID": 1,
            "team1": 1,
            "team2": 2,
            "status": "IN PLAY",
            "num_questions": 2  
        },
        {
            "gameID": 2,
            "team1": 5,
            "team2": 6,
            "status": "IN PLAY",
            "num_questions": 3  
        }
    ]
}
```

## Section 7: Questions Routes

###### **POST /api/questions/<game_id_slug>/**

Inserts a question into the database for the specified gameID. 

*Input* 
```
{
    "api_key": "xxxxxxxxx",
    "worth": 35, (score increase from question)
    "decrease": 5, (score decrease)
    "text": "Over or Under 3.5 goals?",
    "opt1": "over",
    "opt2": "under",
    "opt3": "NULL", 
    "time_designation": "PREGAME"
}
```

*Output* 
```
{
    "text": "Over or Under 3.5 goals?",
    "opt1": "over",
    "opt2": "under",
    "opt3": "NULL", 
    "questionID": 1,
    "answer": "PENDING"
}
```

This route requires a significant amount of information from the backend. When the route is called, each question is inserted into the database with an answer of 'PENDING'. Once the question is updated, this field will contain the actual answer, and can be used to determine the accuracy of user answers. 

###### **POST /api/questions/update/<question_id_slug>/**

Updates the answer field of a question in the database. 

*Input* 
```
{
    "api_key": "xxxxxxxxxx",
    "answer": "over"
}
```
*Output* 
```
{
    "num_correct": 2, (number of correct users)
    "num_incorrect": 5, (number of incorrect users)
    "increase": 35, (score increase)
    "decrease": 5 (score decrease)
}
```

After this route is called, each user's answer for the particular question is cross checked with the newly inserted correct answer. If the user is correct, their score is updated with the 'worth' parameter, if not, their score is decreased by the 'decrease' parameter. 

###### **GET /api/questions/<game_id_slug>/**

Fetches all the questions pertaining to a specific gameID. 

*Input*
```
{
    "api_key": "xxxxxxxxx"
}
```
*Output* 
```
{
    "questions": [
        {
            "questionID": 1,
            "gameID": 1,
            "worth": 35,
            "decrease": 5,
            "text": "Over or Under 3.5 goals?",
            "options": [
                "over",
                "under",
                "NULL"
            ]
            "answer": "over"
        }
    ]
}
```

Questions are fetched whether they have been completed or not. 

## Section 8: Answers Routes

###### **POST /api/answers/<question_id_slug>/<user_id_slug>/**

Inserts an answer to a particular question, for a particular user. 

*Input* 
```
{
    "api_key": "xxxxxxxx",
    "answer": "over"
}
```
*Output* 
```
{
    "user_id": 1,
    "question_id": 2,
    "answer": "over",
    "status": "PENDING"
}
```

All answers are inserted with a 'PENDING' status. The status is updated upon insertion of the answer to a particular question. Statuses are updated alongside user scores. 