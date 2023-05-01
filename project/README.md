# Project Explanation


The entire application Urls is within the app `project`.

There are two apps setup,  `users` and `user_interests`.

`Users` App is for Signin, Singup flows and to update User basic details
`User Interests` App is to record user's responses to images and history.

`views.py` contains the whole logic of the APIs .
`serializers.py` contains the logic to convert complex data types like queryset to json


# Assumptions
1. When User does not rate a image for 5 seconds, the image is by default considered as rejected by user
2. The timer of 5 seconds for above use case will be taken care by Mobile Application.
3. When user rates a image for the second time, a new row is not created int he DB for the change, instead the same row will be updated.
4. The User will not be shown any images until he completes his profile, which is uodating his username. And this will be taken by Mobile Application again.


Documentation below.

In `settings.py` in DATABASES please input your own Id and password for the database and create a database in your pgAdmin panel.

### Make a virtual enviroment
   
    Recommended python version -----> 3.9.X (The LATEST STABLE RELEASE)
    python -m venv myvenv

### Run the virtual enviroment

    myvenv\Scripts\activate.bat

### Install all dependencies

    pip install  -r requirements.txt

### Migrate

    python manage.py migrate
    
### Run the App
    
    python manage.py runserver

# REST API

The REST API to the  app is described below.

## Genearete OTP
   Generates on OTP for the given Mobile Number

### POST Request

`POST /api/users/generate_otp/`

#### body
    {
        "phone_number": "+918125825876"
    }


### Response
    
    {
        "success": true,
        "total_count": null,
        "next": null,
        "previous": null,
        "next_page": null,
        "current_page": null,
        "previous_page": null,
        "page_size": null,
        "data": {
            "message": "OTP Sent Successfully",
            "phone_number": "+918074751371"
        }
    }

----------------------------------------------------------------------------------------------------------------------------

## Verify OTP
API to validate the OTP received by user. This API also creates user with the given phone number.
And the same can be used to login a user with existing phone number.

### POST Request

`POST /api/users/verify_otp/` 

#### body
    {
        "phone_number": "+918125825876",
        "otp_received": "00000"
    }
     
### Response

    {
        "success": true,
        "total_count": null,
        "next": null,
        "previous": null,
        "next_page": null,
        "current_page": null,
        "previous_page": null,
        "page_size": null,
        "data": {
            "display_message": "OTP Verified Successfully",
            "phone_number": "+918074751371",
            "user": {
                "id": 2,
                "username": "+918074751371",
                "phone_number": "+918074751371",
                "is_profile_complete": false,
                "token": "ddaa2531a0bcf9ed61bcfd2de260c82a01770187",
                "created_at": "2023-05-01T16:12:52.867399Z",
                "modified_at": "2023-05-01T16:12:52.867407Z"
            }
        }
    }

    
-------------------------------------------------------------------------------------------------------------------------------   

## Update Username for user

### PATCH Request

`PATCH /api/users/2/`

#### body
    {
        "username": "Ganesh123"
    }

#### Headers
    {
        "Authorization": f"Token {user_token}"
    }

### Response

    {
        "success": true,
        "total_count": null,
        "next": null,
        "previous": null,
        "next_page": null,
        "current_page": null,
        "previous_page": null,
        "page_size": null,
        "data": {
            "id": 1,
            "username": "Ganesh12",
            "phone_number": "+918125825876",
            "is_profile_complete": true,
            "token": "5fdb53552b582fcf2d76891211c6524cb72639d2",
            "created_at": "2023-05-01T12:36:25.478064Z",
            "modified_at": "2023-05-01T12:36:53.799713Z"
        }
    }
-------------------------------------------------------------------------------------------------------------------------

## Get Images for Home Screen

### GET Request
According to the current Floor of the elevator this api will show direction

`GET /api/images`

#### Headers
    {
        "Authorization": f"Token {user_token}"
    }

### Response

    {
        "success": true,
        "total_count": 5,
        "next": null,
        "previous": null,
        "next_page": null,
        "current_page": 1,
        "previous_page": null,
        "page_size": 10,
        "data": [
            {
                "id": 1,
                "created_at": "2023-05-01T12:35:24.490424Z",
                "modified_at": "2023-05-01T12:35:24.490434Z",
                "name": "One",
                "image_url": "http://getdrawings.com/one-icon#one-icon-3.png"
            },
            {
                "id": 2,
                "created_at": "2023-05-01T12:35:24.490444Z",
                "modified_at": "2023-05-01T12:35:24.490448Z",
                "name": "Two",
                "image_url": "http://getdrawings.com/free-shirt-icon#free-shirt-icon-9.png"
            },
            {
                "id": 3,
                "created_at": "2023-05-01T12:35:24.490456Z",
                "modified_at": "2023-05-01T12:35:24.490460Z",
                "name": "Three",
                "image_url": "http://getdrawings.com/serial-number-icon#serial-number-icon-19.png"
            },
            {
                "id": 4,
                "created_at": "2023-05-01T12:35:24.490467Z",
                "modified_at": "2023-05-01T12:35:24.490471Z",
                "name": "Four",
                "image_url": "http://getdrawings.com/serial-number-icon#serial-number-icon-18.png"
            },
            {
                "id": 5,
                "created_at": "2023-05-01T12:35:24.490478Z",
                "modified_at": "2023-05-01T12:35:24.490482Z",
                "name": "Five",
                "image_url": "http://getdrawings.com/number-one-icon#number-one-icon-17.png"
            }
        ]
    }

--------------------------------------------------------------------------------------------------------------------------    

## Create or Update User rating for a image

### POST Request

`POST /api/user_ratings/` 

#### body
    {
        "image_id": 5,
        "selection_type": "interested"
    }
#### Headers
    {
        "Authorization": f"Token {user_token}"
    }
    
### Response
    
    {
        "success": true,
        "display_message": "Mahesh12, you have rated all the images. Thank You!",
        "total_count": null,
        "next": null,
        "previous": null,
        "next_page": null,
        "current_page": null,
        "previous_page": null,
        "page_size": null,
        "data": {
            "id": 5,
            "image": {
                "id": 5,
                "created_at": "2023-04-30T20:34:59.650953Z",
                "modified_at": "2023-04-30T20:34:59.650957Z",
                "name": "Five",
                "image_url": "http://getdrawings.com/number-one-icon#number-one-icon-17.png"
            },
            "user": {
                "id": 2,
                "username": "Mahesh12",
                "phone_number": "+918074751370",
                "is_profile_complete": true,
                "token": "9de51abe1dd875754d5bf1b66297cd880f193e39",
                "created_at": "2023-04-30T20:08:58.072047Z",
                "modified_at": "2023-04-30T20:29:09.032686Z"
            },
            "selection_type": "interested"
        }
    }
       

### GET User rating history

`GET /api/user_ratings`

#### Headers
    {
        "Authorization": f"Token {user_token}"
    }

#### Response
    {
        "success": true,
        "display_message": null,
        "total_count": 5,
        "next": null,
        "previous": null,
        "next_page": null,
        "current_page": 1,
        "previous_page": null,
        "page_size": 10,
        "data": [
            {
                "id": 1,
                "image": {
                    "id": 1,
                    "created_at": "2023-04-30T20:34:59.650884Z",
                    "modified_at": "2023-04-30T20:34:59.650906Z",
                    "name": "One",
                    "image_url": "http://getdrawings.com/one-icon#one-icon-3.png"
                },
                "user": {
                    "id": 2,
                    "username": "Mahesh12",
                    "phone_number": "+918074751370",
                    "is_profile_complete": true,
                    "token": "9de51abe1dd875754d5bf1b66297cd880f193e39",
                    "created_at": "2023-04-30T20:08:58.072047Z",
                    "modified_at": "2023-04-30T20:29:09.032686Z"
                },
                "selection_type": "rejected"
            },
            {
                "id": 2,
                "image": {
                    "id": 2,
                    "created_at": "2023-04-30T20:34:59.650916Z",
                    "modified_at": "2023-04-30T20:34:59.650922Z",
                    "name": "Two",
                    "image_url": "http://getdrawings.com/free-shirt-icon#free-shirt-icon-9.png"
                },
                "user": {
                    "id": 2,
                    "username": "Mahesh12",
                    "phone_number": "+918074751370",
                    "is_profile_complete": true,
                    "token": "9de51abe1dd875754d5bf1b66297cd880f193e39",
                    "created_at": "2023-04-30T20:08:58.072047Z",
                    "modified_at": "2023-04-30T20:29:09.032686Z"
                },
                "selection_type": "rejected"
            },
            {
                "id": 3,
                "image": {
                    "id": 3,
                    "created_at": "2023-04-30T20:34:59.650929Z",
                    "modified_at": "2023-04-30T20:34:59.650934Z",
                    "name": "Three",
                    "image_url": "http://getdrawings.com/serial-number-icon#serial-number-icon-19.png"
                },
                "user": {
                    "id": 2,
                    "username": "Mahesh12",
                    "phone_number": "+918074751370",
                    "is_profile_complete": true,
                    "token": "9de51abe1dd875754d5bf1b66297cd880f193e39",
                    "created_at": "2023-04-30T20:08:58.072047Z",
                    "modified_at": "2023-04-30T20:29:09.032686Z"
                },
                "selection_type": "rejected"
            },
            {
                "id": 4,
                "image": {
                    "id": 4,
                    "created_at": "2023-04-30T20:34:59.650941Z",
                    "modified_at": "2023-04-30T20:34:59.650946Z",
                    "name": "Four",
                    "image_url": "http://getdrawings.com/serial-number-icon#serial-number-icon-18.png"
                },
                "user": {
                    "id": 2,
                    "username": "Mahesh12",
                    "phone_number": "+918074751370",
                    "is_profile_complete": true,
                    "token": "9de51abe1dd875754d5bf1b66297cd880f193e39",
                    "created_at": "2023-04-30T20:08:58.072047Z",
                    "modified_at": "2023-04-30T20:29:09.032686Z"
                },
                "selection_type": "rejected"
            },
            {
                "id": 5,
                "image": {
                    "id": 5,
                    "created_at": "2023-04-30T20:34:59.650953Z",
                    "modified_at": "2023-04-30T20:34:59.650957Z",
                    "name": "Five",
                    "image_url": "http://getdrawings.com/number-one-icon#number-one-icon-17.png"
                },
                "user": {
                    "id": 2,
                    "username": "Mahesh12",
                    "phone_number": "+918074751370",
                    "is_profile_complete": true,
                    "token": "9de51abe1dd875754d5bf1b66297cd880f193e39",
                    "created_at": "2023-04-30T20:08:58.072047Z",
                    "modified_at": "2023-04-30T20:29:09.032686Z"
                },
                "selection_type": "rejected"
            }
        ]
    }
--------------------------------------------------------------------------------------------------------------------   


# Swagger Postman documentation Link
``

# Video Demonstrating the APP Flows
``
