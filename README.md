## Banter API Documentation

By: Colin McGravey

#### Section 1: Scripts

###### bin/run_db (create | destroy | reset | dump)

The db script can be run from the command line and must be run with one keyword argument (create, destroy, reset, or dump). Running the script with 'dump' specified will dump all tables of the database into output. Create, destroy, reset, all deal with tearing down the database or initializing. 

###### bin/run_api

This script takes no keyword arguments, and simply runs the flask application on your local machine on port 8000. 

###### bin/test_api

This script also takes no keyword arguments and runs through a mock use case of the API, inserting users, questions, answers, and updating user scores. 


#### Section 2: Basic Request Syntax 
All requests should be made with a JSON body. Inside the JSON, for every request made, include the private API key in a field titled "api_key". Each request will demand for different fields to be included and will be explained later in this document. The only route that can be accessed with no API key is http://localhost:8000/api/routes/, which displays the possible API endpoints. 

This documentation is written assuming the API is running on your local machine, however, if it is in some deployed environment, the request URLs should be changed accordingly. 


###### Example: JSON body for request

{
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"api_key": "xxxxxxxxxxx",
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"username": "cmcgravey",
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"password": "password"
}

#### Section 3: Routes Endpoint

###### http://localhost:8000/api/routes/

Request body is unneccessary for this route as it does not require an API key, nor any extraneous information. Response will be in the form ...

{
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"routes": "GET /api/routes/",
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**"users"**: [
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"insert_user": "POST /api/users/"},
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"fetch_user": "GET /api/users/<user_id_slug>/"},
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"update_user": "POST /api/users/<user_id_slug>/"},
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"logon_user": "POST /api/users/logon/"}
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;],
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**"teams"**: [
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"insert_team": "POST /api/teams/"}, 
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"fetch_team": "GET /api/teams"}
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;],
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**"games"**: [
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"insert_game": "POST /api/games/"},
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"update_game": "POST /api/games/<game_id_slug>/"},
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"fetch_one": "GET /api/games/<game_id_slug>/"},
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"fetch_multiple": "GET /api/games/"}
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;], 
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**"answers"**: [
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"insert_answer": "POST /api/answers/<question_id_slug>/"}
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;],
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**"questions"**: [
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"insert_question": "POST /api/questions/<game_id_slug>/"},
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"update_question_answer": "POST /api/questions/update/<question_id_slug>/"},
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"fetch_game_questions": "GET /api/questions/<game_id_slug>/"}
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]
}

**The remainder of the documentation will be split into these five sections.** 

#### Section 4: User Routes

###### - **POST /api/users/**

This route will insert a user into the database. 

*Input* {
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"api_key": "xxxxxxxxxxx",
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"username": "cmcgravey", 
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"password": "password" 
}

*Output* {
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"userID": 1,
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"username": "cmcgravey",
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"banter": 0
}

###### - **POST /api/users/<user_id_slug>/**

Updates a user's password or score

*Input* {
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"api_key": "xxxxxxxx",
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"type": "password" || "banter",
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"new_banter": 45,
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"new_password": "password"
}
*Output* {
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"userID": 1,
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"username": "cmcgravey",
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"banter": 0
}

If the route is being utilized for a password update, do not include the field "new_banter". The same is true for if you are updating banter score, do not include the field "new_password".

###### - **POST /api/users/logon/**

Route simulates logging on a user, receives a username and password and determines if the information is valid. 

*Input* {
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"api_key": "xxxxxxxxx",
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"username": "cmcgravey",
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"password": "password"
}
*Output #1* {
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"userID": 1,
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"username": "cmcgravey",
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"banter": 0
}
*Output #2* {
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"msg": "Invalid Password"
}
*Output #3* {
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"msg": "Invalid User"
}

Outputs 2 and 3 result from invalid information being given to the API. 

###### - **GET /api/users/<user_id_slug>/**

Route fetches the information for one user by userID. 

*Input* {
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"api_key": "xxxxxxxxx"
}
*Output* {
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"userID": 1,
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"username": "cmcgravey",
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"banter": 0
}

#### Section 5: Teams Routes

###### **- POST /api/teams/**

Inserts a team into the database.

*Input* {
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"api_key": "xxxxxxxx",
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"name": "Chelsea", 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"abbr": "CHE",
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"logo": "chelsea.png"
}
*Output* {
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"teamID": 1,
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"name": "Chelsea"
}

###### **-GET /api/teams/<team_id_slug>/**

Fetches team from the database according to teamID. 

*Input* {
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"api_key": "xxxxxxxx"
}
*Output* {
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"name": "Chelsea",
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"abbr": "CHE",
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"logo": "chelsea.png",
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"teamID": 1
}

#### Section 6: Games Routes

###### **- POST /api/games/
