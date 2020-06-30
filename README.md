# Full-Stack-Developer Nanodegree

This repository includes the different work files of the Udacity Full-Stack-Developer nanodegree that focuses mostly on backend development with a bit of frontend development for visual rendering and web browser interactions with the backend.
The tech stack that I used all along is mostly Python and some inputs of JavaScript, HTML and CSS.


## Project 1: Fyurr booking app

This app was meant to be able to join the artists and the venues. It allows artists to list themselves on the platform and the same for the venues. Then each of them would indicate if they were looking for venues and talents respectively. Finally, the artists could list concerts by joining their profile to the venue and display all these informations at once.

<u>Tech stack</u>:

- `Python`
- `SQLAlchemy`
- `Flask`
- `PostgreSQL`


## Project 2: Trivia API

This second project was aimed at interfacing an SQL database with a `React` frontend to manage the questions of a Trivia game. These questions would later be used to power the Quizz Gameplay.

<u>Tech stack</u>:

- `React` (already implemented in the starter code) for the browser interaction
- `Python` for the backend code
- `Flask` as the basis of the backend
- `CORS` for handling one page interaction
- `unittest` to test the different endpoints
- `curl` to test the requests with command line instead of browser


## Project 3: Coffee shop full stack

The third project was designed to implement authentification methods based on Json Web Token (JWT) to control the access to the app.

<u>Tech stack</u>:

- `Python` for the backend code
- `Flask` as the basis of the backend
- `Ionic` for the frontend (already implemented in the starter code)
- `Auth0` to power the authentification and permission service
- `jose` for encoding and decoding the JWT tokens
- `Postman` to have a visual interface when making requests to the website
- `curl` to make requests directly from the terminal

## Project 4: Containerize and deploy an app on AWS EKS

Finally before jumping into the capstone project, I have explored the CI/CD pipelines and containerization with Docker.

<u>Tech stack</u>:

- `Python` for the backend code
- `Flask` as the basis of the backend
- `Docker` to containerize my app
- `AWS EKS` to host the container on Kubernetes
- `awscli` to in 
- `kubectl` to interact with Kubernetes clusters and pods (from the Terminal)
- `ekscli` to crete the container from the Terminal

## Project 5: Capstone project

For this final project, I have decided to go with the plan that was advised: building an API than stores actors and movies information into a database. Furthermore, it includes some identification to monitor the access and permissions of users.

<u>Tech stack</u>:

- `Python` for the backend code
- `Flask` as the basis of the backend
- `PostgreSQL` to host the data of actors and movies
- `Heroku` to deploy the app on the web
- `Auth0` to power the authentification and permission service
- `jose` for encoding and decoding the JWT tokens
- `Postman` to have a visual interface when making requests to the website
- `curl` to make requests directly from the terminal
