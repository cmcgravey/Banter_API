# Banter API Documentation

By: Colin McGravey

### <em>Table of Contents</em>
**[Section 1: Scripts](#scripts)**<br>
**[Section 2: Basic Request Syntax](#basic-request-syntax)**<br>
**[Section 3: Routes](#routes)**<br>
**[Section 4: Users](#users)**<br>
**[Section 5: Teams](#teams)**<br>
**[Section 6: Games](#games)**<br>
**[Section 7: Questions](#questions)**<br>
**[Section 8: Answers](#answers)**<br>


## Scripts 

#### 1. ./bin/run_db (create | destroy | reset | dump)

The db script can be run from the command line and must be run with one keyword argument (create, destroy, reset, or dump). Running the script with 'dump' specified will dump all tables of the database into output. Create, destroy, reset, all deal with tearing down the database or initializing. 

#### 2. ./bin/run_api

This script takes no keyword arguments, and simply runs the flask application on your local machine on port 8000. 

#### 3. ./bin/test_api (deployed | local)

This script takes one keyword argument, determining whether to test the API running on your local machine, or the API running on AWS. It then runs through a mock use case of the API, inserting users, questions, answers, and updating user scores.


## Basic Request Syntax 
All routes can be accessed on your local machine at http://localhost:8000/api/routes/ or on the actual instance, running at https://www.banter-api.com/api/routes/.

All <b>POST</b> requests should be made with a JSON body. Inside the JSON, for every request made, include the private API key in a field titled "api_key". Each request will demand for different fields to be included and will be explained later in this document. All <b>GET</b> requests take the API key as a URL keyword argument. The only route that can be accessed with no API key is /api/routes/, which displays the possible API endpoints. 


###### Example: JSON body for POST request

```
{
    "api_key": "xxxxxxxxxxx",
    "username": "cmcgravey",
    "password": "password"
}
```
###### Example: URL for GET request
```
http://localhost:8000/api/users/1/?api_key=xxxxxxx
```

## **Routes**

#### **GET /api/routes/**

Request body is unneccessary for this route as it does not require an API key, nor any extraneous information. Response will be in the following form ...

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

## **Users**

#### **GET /api/users/**

Inserts one user into the database. 

*Input* 
```
{
    "api_key": "xxxxxxxxxxx",
    "username": "cmcgravey", 
    "password": "password", 
    "full_name": "Colin McGravey"
}
```

*Output* 
```
{
    "userID": 1,
    "username": "cmcgravey",
    "full_name": "Colin McGravey",
    "banter": 0
}
```

#### **POST /api/users/<user_id_slug>/**

Updates a user's password or score.

*Input* 
```
{
    "api_key": "xxxxxxxx",
    "type": "password",
    "new_password": "password"
}
OR 
{
    "api_key": "xxxxxxxx",
    "type": "banter",
    "new_banter": 50
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

The "type" key determines which update will occur. The third field corresponds to type, and can either be "new_password" or "new_banter", containing a string and an integer, respectively. 

#### **POST /api/users/logon/**

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

Outputs 2 and 3 result from invalid password or username being given to the API, respectively. 

#### **GET /api/users/<user_id_slug>/?api_key=xxxx**

Route fetches the information for one user by userID. 

*Output* 
```
{
    "userID": 1,
    "username": "cmcgravey",
    "banter": 0, 
    "full_name": "Colin McGravey"
}
```

#### **GET /api/users/leaders/?api_key=xxxx**
Fetches the top five users by banter score. 

*Output*
```
{
    "leaders": [
        {"name": "cmcgravey", "banter": 100},
        {"name": "ianglee", "banter": 96},
        {"name": "samimud", "banter": 94},
        {"name": "wraineri", "banter": 26},
        {"name": "cvenuti", "banter": 20}
    ]
}
```

## Teams

#### **POST /api/teams/**

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

#### **GET /api/teams/<team_id_slug>/?api_key=xxxxx**

Fetches team from the database according to teamID. 

*Output* 
```
{
    "name": "Chelsea",
    "abbr": "CHE",
    "logo": "chelsea.png",
    "teamID": 1
}
```

## Games

#### **POST /api/games/**

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

#### **POST /api/games/<game_id_slug>/**

Updates the score of a game and time elapsed, also can be used to update the game status. Game statuses can be one of three values in the database, 'PENDING', 'PREGAME', 'IN PLAY', or 'COMPLETE'.

*Input* 
```
{
    "api_key": "xxxxxxxxxx",
    "update": [1, 0, "23:42"]
}
OR
{
    "api_key": "xxxxxxx",
    "update": [0, 0, "00:00"],
    "status": "IN PLAY"
}
```
*Output* 
```
{
    "gameID": 1,
    "team1": 1,
    "team1_score": 1,
    "team2": 2,
    "team2_score": 0,
    "time_elapsed": "23:42"
    "status": "IN PLAY",
    "num_questions": 0
}
```

Every time the route is used, an "update" field must be specified. The "status" field is completely optional, if specified, the status of the game will also be updated. 

#### **GET /api/games/<game_id_slug>/?api_key=xxxxx**

Fetches one game by gameID. 

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

#### **GET /api/games/status/<status_slug>/?api_key=xxxx**

Fetches all games of a particular status, i.e. 'PENDING', 'IN PLAY', 'COMPLETED'.

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

The <status_slug> argument must be one of the specified statuses, 'PENDING', 'PREGAME', 'IN PLAY', or 'COMPLETE'.

## Questions

#### **POST /api/questions/<game_id_slug>/**

Inserts a question into the database for the specified gameID. 

*Input* 
```
{
    "question_stage": "Pregame",
    "label": "h2h",
    "question": "Who is going to win?",
    "Game_id": 12,
    "opt1": [
        "Everton",
        15,
        6
    ],
    "opt2": [
        "Liverpool",
        36,
        14
    ],
    "opt3": [
        "Draw",
        17,
        6
    ]
}
```

*Output* 
```
{
    "text": "Who is going to win?", 
    "opts": ["Everton", "Liverpool", "Draw"], 
    "questionID": 1,
    "answer": "PENDING",
    "label": "h2h",
    "stage": "Pregame"
}
```

This route requires a significant amount of information from the backend. When the route is called, each question is inserted into the database with an answer of 'PENDING'. Once the question is updated, this field will contain the option for the answer, and can be used to determine the accuracy of user answers. 

#### **POST /api/questions/update/<question_id_slug>/**

Updates the answer field of a question in the database. 

*Input* 
```
{
    "api_key": "xxxxxxxxxx",
    "answer": "opt1"
}
```
*Output* 
```
{
    "num_correct": 2, (number of correct users)
    "num_incorrect": 5, (number of incorrect users)
    "increase": 15, (score increase)
    "decrease": 6 (score decrease)
}
```

After this route is called, each user's answer for the particular question is cross checked with the newly inserted correct answer. If the user is correct, their score is updated with the 'worth' parameter, if not, their score is decreased by the 'decrease' parameter. <b>IMPORTANT</b>: When the answer is inserted it must be one of the three strings ['opt1', 'opt2', 'opt3'], else there will be serious errors. 

#### **GET /api/questions/<game_id_slug>/?api_key=xxxx**

Fetches all the questions pertaining to a specific gameID. 

*Output* 
```
{
    "questions": [
        {
            "questionID": 1,
            "gameID": 1,
            "text": "Who is going to win?",
            "label": "h2h",
            "stage": "Pregame",
            "options": [
                "Everton",
                "Liverpool",
                "Draw"
            ],
            "increases": [
                15,
                36, 
                17
            ],
            "decreases": [
                6, 
                14, 
                6
            ],
            "answer": "over"
        }
    ]
}
```

Questions are fetched whether they have been resolved or not, i.e. whether their answer is decided or still 'PENDING'.

## Answers

#### **POST /api/answers/<question_id_slug>/<user_id_slug>/**

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

All answers are inserted with a 'PENDING' status. The status is updated upon insertion of the answer to a particular question. Statuses are updated alongside user scores. The actual answer should always be inserted as one of ['opt1', 'opt2', 'opt3']. The answer should not be answered as the literal text for the option, this will cause serious issues. 

#### **GET /api/answers/<question_id_slug>/<user_id_slug>/?api_key=xxxx**

Returns whether a user has logged an answer for a particular question or not, along with their answer if True. 

*Output*
```
{
    "answered": False,
    "answer": None
}
OR 
{
    "answered": True, 
    "answer": opt1
}
```