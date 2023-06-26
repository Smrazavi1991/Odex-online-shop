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
- Homepage with showing discounted products

![homepage](https://github.com/Smrazavi1991/Django-online-shop-Project/assets/121284960/d4b5eaf1-c931-4872-be2d-1ec4ad1bd7a3)

- Admin panels

![admin panel2](https://github.com/Smrazavi1991/Django-online-shop-Project/assets/121284960/89128eb3-d029-40ef-bb0a-d96bc00438af)
![admin panel](https://github.com/Smrazavi1991/Django-online-shop-Project/assets/121284960/59e02f7c-f704-4c5c-b4c4-855c6ac2a65d)

- Cart page

![cart](https://github.com/Smrazavi1991/Django-online-shop-Project/assets/121284960/4ce2e0a8-f61e-4866-a51b-93ebd6b9d8e9)

- Review order page
  
![review order](https://github.com/Smrazavi1991/Django-online-shop-Project/assets/121284960/34e45e0d-22cf-4a5d-b038-ae48d90b32d0)

- Profile pages:
    -  User information page

     ![profile](https://github.com/Smrazavi1991/Django-online-shop-Project/assets/121284960/9f3770c7-743d-4bd5-81bd-006377499ed5)

    - User Change password page

     ![change pass](https://github.com/Smrazavi1991/Django-online-shop-Project/assets/121284960/2203f81e-84af-45a1-9941-84f1d9910c79)

    - User addresses page
 
    ![user addresses](https://github.com/Smrazavi1991/Django-online-shop-Project/assets/121284960/4f963fe0-08eb-415f-a05f-2d7b0793dc91)

    - User orders list page
 
    ![user order page](https://github.com/Smrazavi1991/Django-online-shop-Project/assets/121284960/17bf6bd3-80e8-49a0-849d-d93055cfb4df)

    - User orders details page
 
    ![each order detail](https://github.com/Smrazavi1991/Django-online-shop-Project/assets/121284960/a62f93b7-cc5d-498a-b96e-073bef9c9884)

    - User order tracking page
 
    ![tracking order](https://github.com/Smrazavi1991/Django-online-shop-Project/assets/121284960/8f859bb5-7770-466c-a3d8-ee88e9e99b2e)

- User register / login pages:
    - Register page

    ![register page](https://github.com/Smrazavi1991/Django-online-shop-Project/assets/121284960/2e156ce4-31df-4d73-bc78-c36ed2fab6d8)

    - Login page
 
    ![login_page](https://github.com/Smrazavi1991/Django-online-shop-Project/assets/121284960/1bdcb1d4-5590-4762-a777-c0ea75390305)

    - Login with OTP page
 
    ![OTP](https://github.com/Smrazavi1991/Django-online-shop-Project/assets/121284960/6848619b-9de4-4a38-bcb5-3ed52eb01a93)

  

## Setup
This project has several requirement packages that listed in requirements.txt file in project root directory.

To start work with project:  

1- Clone the project repo with `git clone`.  

![clone](https://github.com/Smrazavi1991/Django-online-shop-Project/assets/121284960/ed50d644-8dba-46ca-9137-aa7c3bd28d72)

2- Cd to project root directory "src" and create a virtual environment.

3- Activate virtual environment.

4- Install project requirement packages with `pip install -r requirements.txt`

5- Create a db in postgres with name "odexshop"

6- Create a secrets.py file in src/config directory and place your own SECRET_KEY, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DATABASE_PASSWORD and API_KEY for otp SMS sending API parameters in it.

![secrets](https://github.com/Smrazavi1991/Django-online-shop-Project/assets/121284960/8dcb8fd1-aab6-4fa2-889b-a2aad0aa7557)

7- Create migration files with `python manage.py makemigrations`

8- Migrate with `python manage.py migrate`

9- Create a superuser account with `python manage.py createsuperuser` and enter the requested items.

10- Run it with `python manage.py runserver`


## Project Status
Project is:  _complete_


## Room for Improvement
There are many things can be done to improve projects. but some of most important things is:

To do:
- Add contact-us functionality
- Add comment feature on posts 
- Add wishlist functionality for users


## Contact
Created by [@Sayyed Mohammad Razavi](https://www.github.com/Smrazavi1991) - feel free to contact me!


<!-- Optional -->
<!-- ## License -->
<!-- This project is open source and available under the [... License](). -->

<!-- You don't have to include all sections - just the one's relevant to your project -->
