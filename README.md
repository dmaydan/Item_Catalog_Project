# Item Catalog
The is my project submission for Udacity's Full Stack Web Developer nanodegree's item catalog project. The goal of the project was to develop an application that provides a list of items within a variety of categories as well as to provide a user registration and authentication system. Registered users have the ability to post, edit and delete their own items. For every item, the website also offers a JSON endpoint. In order to access this endpoint, simply add `'JSON/'` to the end of the URL for a specific item. 
## Demo
A live demo of the project hosted by heroku is avaliable at https://item-catalog-proj.herokuapp.com
## Screenshots
### Logged In
#### Catalog
[](readme_images/out_catalog.png)
## Backend
### Server
The server is built on the python web framework [Flask](http://flask.pocoo.org). 
### Database 
The website uses a postresql database with 3 tables: user, category, item. 
### Authentication
Google's OAuth2 is implemented as a third party authentication and authorization service.
### Authorization
A user can only create an item if he/she is logged in, and a user can only edit item that he/she created. If a logged out user tries to create/edit/delete an item, he/she will be redirected to the login page. If a logged in user tries edit/delete an item he/she did not create, he/she will receive a javascript warning and not be able to complete the action.
## Frontend
### Responsive
A media query is used to ensure that content looks great on all display sizes.
### CSS Grids
The page is layed out with the CSS Grid
## Interactive
After a user completes an action (login, logout, create/edit/delete item) and the site redirects, a flash message is displayed to the user to confirm that his/her action was processed.
## Run on your Own
Note: in order to actually run this website on your own, you would need to create and fill a database and get google oauth2 credentials. 
