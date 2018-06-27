# Item Catalog
The is my project submission for Udacity's Full Stack Web Developer nanodegree's item catalog project. The goal of the project was to develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users have the ability to post, edit and delete their own items. For every item, the website also contains a JSON endpoint: simply add JSON/ to the URL for that item. 
## Demo
A live demo of the project hosted by heroku is avaliable at https://item-catalog-proj.herokuapp.com
## Backend
### Server
The server is built on the python web framework [Flask](http://flask.pocoo.org). 
### Database 
The website uses a postresql database with 3 tables: user, category, item. 
### Authentication
Google's OAuth2 is implemented as a third party authentication and authorization service.
## Frontend

Note: in order to actually run this website on your own, you would need to create and fill a database and get google auth credentials.
