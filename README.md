# CySec Game

## Front End
Commands to be executed while in `frontend` directory.
### Installation
`npm install`

### Run
`ng serve --open`

(If there is an issue finding the `ng` binary, try running `npx ng serve --open`.)


## Back End
Commands to be executed while in `backend/api` directory.

### Installation
In the backend directory, run:

 `python3 -m pip install -r requirements.txt`

If that does not work or if the `requirements.txt` file is out-of-date, run the following in the `backend/api` directory:

`python3 -m pip install Django djangorestframework django-cors-headers nashpy`

In the `backend/api` directory, run the following: 

`python3 -m pip install nashpy`


### Run 
`python3 manage.py runserver`