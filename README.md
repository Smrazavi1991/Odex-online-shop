# Django online shop Project

> this project is about a simple online shop.
<!-- > Live demo [_here_](https://www.example.com). <!-- If you have the project hosted somewhere, include the link here. -->

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)
<!-- * [License](#license) -->


## General Information
This project is actually an online shop where admins can manage products and users and users can make purchases, that was done as the final project of my Python- Django course.


## Technologies Used
- Python - version 3.9 & 3.10
- Django - version 4.1.9
- Django Rest Framework - version 3.14.0
- Postgre SQL - version 15.0
- HTML & CSS - version 5.0
- JavaScript - version 1.5


## Features
List the ready features here:
- Great user experience
- discount coupons supported
- Use JWT to improve its security
- User login with OTP (email and mobile phone) provided. (note: Because Celery is used in the otp sending process and Celery does not have an official version for Windows, it is highly recommended to load the project on Linux to get the best performance.)  


## Screenshots
![Example screenshot](./img/screenshot.png)
<!-- If you have screenshots you'd like to share, include them here. -->


## Setup
This project has several requirement packages that listed in requirements.txt file in project root directory.

To start work with project:  

1- clone the project repo with `git clone`.  

![clone](https://github.com/Smrazavi1991/Django-online-shop-Project/assets/121284960/2da286fd-b182-49f4-871a-7638a3a97e90)

2- cd to project root directory "src" and create a virtual environment.

3- activate virtual environment.

4- install project requirement packages with `pip install -r requirements.txt`

5- create a db in postgres with name "odexshop"

6- create a secrets.py file in src/config directory and place your own SECRET_KEY, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD and DATABASE_PASSWORD parameters in it.

7- create migration files with

8- migrate with

9- create a superuser account with

10- run it with
Proceed to describe how to install / setup one's local environment / get started with the project.


## Project Status
Project is:  _complete_


## Room for Improvement
Include areas you believe need improvement / could be improved. Also add TODOs for future development.

Room for improvement:
- Improvement to be done 1
- Improvement to be done 2

To do:
- Feature to be added 1
- Feature to be added 2


## Acknowledgements
Give credit here.
- This project was inspired by...
- This project was based on [this tutorial](https://www.example.com).
- Many thanks to...


## Contact
Created by [@flynerdpl](https://www.flynerd.pl/) - feel free to contact me!


<!-- Optional -->
<!-- ## License -->
<!-- This project is open source and available under the [... License](). -->

<!-- You don't have to include all sections - just the one's relevant to your project -->
