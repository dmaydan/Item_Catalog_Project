<h1>Item Catalog</h1>
The is my project submission for Udacity's Full Stack Web Developer nanodegree's item catalog project. The goal of the project was to develop an application that provides a list of items within a variety of categories as well as to provide a user registration and authentication system. Registered users have the ability to post, edit and delete their own items. For every item, the website also offers a JSON endpoint. In order to access this endpoint, simply add <code>'JSON/'</code> to the end of the URL for a specific item.
<h2>Outline</h2>
<ol>
<li><a href="#demo">Demo</a></li>
<li><a href="#run">Run on your Own</a></li>
<li><a href="#screenshots">Screenshots</a></li>
<li><a href="#backend">Backend</a></li>
<li><a href="#frontend">Frontend</a></li>
<li><a href="#interactive">Interactive</a></li>
</ol>
<h2 id="demo">Demo</h2>
A live demo of the project hosted by heroku is avaliable at https://item-catalog-proj.herokuapp.com
<h2 id="run">Run your Own</h2>
Note: in order to actually run this website on your own, you would need to create and fill a database and get google oauth2 credentials. 
<h2 id="screenshots">Screenshots</h2>
<h3>Logged Out</h3>
<h4>Catalog</h4>
<img src="readme_images/out_catalog.png" width="300"/>
<h4>Category</h4>
<img src="readme_images/out_category.png" width="300"/>
<h4>Item</h4>
<img src="readme_images/out_item.png" width="300"/>
<h4>404 Error</h4>
<img src="readme_images/out_404.png" width="300"/>
<h4>500 Error</h4>
<img src="readme_images/out_500.png" width="300"/>
<h3>Logged In</h3>
<h4>Catalog</h4>
<img src="readme_images/in_catalog.png" width="300"/>
<h4>Category</h4>
<img src="readme_images/in_category.png" width="300"/>
<h4>Item Created by Current User</h4>
<img src="readme_images/in_my_item.png" width="300"/>
<h4>New Item</h4>
<img src="readme_images/in_new.png" width="300"/>
<h4>Edit Item</h4>
<img src="readme_images/in_edit.png" width="300"/>
<h4>Delete Item</h4>
<img src="readme_images/in_delete.png" width="300"/>
<h4>404 Error</h4>
<img src="readme_images/in_404.png" width="300"/>
<h4>500 Error</h4>
<img src="readme_images/in_500.png" width="300"/>
<h2 id="backend">Backend</h2>
<h3>Server</h3>
The server is built on the python web framework [Flask](http://flask.pocoo.org). 
<h3>Database</h3>
The website uses a postresql database with 3 tables: user, category, item. 
<h3>Authentication</h3>
Google's OAuth2 is implemented as a third party authentication and authorization service.
<h3>Authorization</h3>
A user can only create an item if he/she is logged in, and a user can only edit item that he/she created. If a logged out user tries to create/edit/delete an item, he/she will be redirected to the login page. If a logged in user tries edit/delete an item he/she did not create, he/she will receive a javascript warning and not be able to complete the action.
<h2 id="frontend">Frontend</h2>
<h3>Responsive</h3>
A media query is used to ensure that content looks great on all display sizes.
<h3>CSS Grids</h3>
The page is layed out with the CSS Grid
<h2 id="interactive">Interactive</h2>
After a user completes an action (login, logout, create/edit/delete item) and the site redirects, a flash message is displayed to the user to confirm that his/her action was processed.

