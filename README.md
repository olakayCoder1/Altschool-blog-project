# Altschool Second Semester Examination Project


![image](https://user-images.githubusercontent.com/95700260/200096389-0da5ce67-3664-4a0f-b3a0-041f2c7fb21a.png)


### OVERVIEW

You need to create a blogging app. The fundamental concept is that anyone visiting the website should be able to read a blog post written by them or another user because the app has a landing page that lists a variety of articles written by different authors.

## SPECIFICATIONS


The Blog should have a Home Page, About Page, Contact Page, the Blog application should have a user authentication where a user can create an account and login so that they could be able to create a blog, also the Blog should have the logout ability.

## MILESTONES

- There should be a variety of users who can access the program and contribute content to the blogging platform.
- Every user needs to have a first name, last name, email, and (you can add other attributes you want to store about the user)
- Theblogappshouldallowuserstoregisterandlogin.
- Thehomepageoftheappshouldprovidealistofblogsproducedby various users.
- Each blog should show the user that created it and the time the blog was created.
- Signed in and non signed in users should be able to visit this page
- If a user is signed in and visits an article they created, they should see an edit button to edit either the title or the body of the article.
-  Clicking on the edit button on an article should take the user to the edit page.
- Your database should contain User information and should be able to store every information about the User there.
- Try to be creative as we will be paying attention to the details. 

# FEATURES
- Authentication and authorization 
- Two factor authentication  ( pending)
- Password reset 
- Pagination 
- View , create , update and delete post 
- Add image to post  
- Add profile image 


## ENPOINTS
| ROUTE | FUNCTIONALITY |ACCESS|
| ----- | ------------- | ------------- |
| ```/register``` | _Register new user_| _Any user_|
| ```/login``` | _Login user_| _Any_|
| ```/logout``` | _Logout user_| _Authenticated user_|
| ```/password-reset``` | _Request password reset_| _Any_|
| ```/password-reset``` | _ Change password_| _Authenticated user_|
| ```/password-reset/<token>/<public_id>``` | _Confirm password reset & create new password_| _Any_|
| ```/``` | _Home page_| _Any_|
| ```/posts``` | _Get a posts_| _Authenticated user_|
| ```/posts/<public_id>``` | _Retrive a post_| _Authenticated user_|
| ```/posts/<public_id>/create``` | _Create a post_| _Authenticated user_|
| ```/posts/<public_id>/edit``` | _Edit a post_| _Authenticated user and post author_|
| ```/posts/<public_id>/delete``` | _Delete a post_| _Authenticated user and post author_|
| ```/account``` | _User account_| _Authenticated user_|
| ```/account/edit``` | _Edit account_| _Authenticated user_|
| ```/account/delete``` | _Delete account_| _Authenticated user_|
| ```/contact``` | _Contact_| _Any_|
| ```/about``` | _About xenith_| _Any_|
