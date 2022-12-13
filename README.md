# Traveler Web App - CS50 Final Project 2022

#### Video Demo: https://youtu.be/4BfwX2Xj0z0

#### Description: 
The purpose of this Django web app is to allow users to upload & browse different trip plans. When planning a trip recently, it was frustrating to have to search many different places for itineraries and ideas and I wanted to create something where you could find everything in one place to help you plan your next adventure.

## Distinctiveness and Complexity: 
This project is focused on providing information for travel. Nothing is being sold/bought/auctioned so it is not like an ecommerce site. While it does have different users that can post trip plans, these trip itineraries are different than just making posts on social media. Their purpose is to provide information to help others plan their travels. There is no ability to like/comment on trips so there really is no interaction between the users. It is more complex than previous projects because, while it combines some elements of each of them, it also incorporates a Google Maps Platform API, sortby functionality, the ability to upload, caption, & edit images, a rich-text editor, a photo carousel built from scratch, a navigation dropdown, and mobile-responsiveness. 

## Files
### views.py
The view functions for this web app include: 
- index: loads the index.html page
- login_view: VIA GET displays the login form, VIA POST logs a user in
- logout_view: logs a user out
- register: VIA GET displays the register form, VIA POST registers a new user for the site 
- plan: VIA GET loads the plan a trip form, VIA POST saves all of the trip data into the models & redirects the user to caption the photos they just uploaded
- captions: saves the captions the user enters for each photo
- trip_view: displays a single trip. Takes a trip_id as a parameter and uses that to load the details of the desired trip and display them on the page.
- profile: takes a user id as a parameter and loads the profile page for that user. If it is the profile of the user currently logged in, they will see an option to edit their profile.
- tags: If a user clicks on a tag, it passes in the tag name as a parameter and loads all of the trips for that tag to display on the page.
- browse: Displays all trips with the option to sort by name, date, budget, etc. If a "sort by" option is selected, the order_by value is passed into the function and it loads trips in the appropriate order and sends them back to the page.
- random_trip: Selects a random trip to display to the user
- edit_profile: Allows the user to change their name, profile photo, and home location. 
- lists_view: When clicking on a list link, a parameter of the list name is passed through. If the list name passed in is "mine", trips that user created will be loaded and displayed. If the list name passed in is "more", all lists for that user will be loaded. Then, when they click on a list, that list name is passed back to the function and all trips on that list for that user will be loaded.
- search: When the user enters a search, it is passed into the function and Trips is filtered using "icontain" to see if the search query is present in the trip title, location, or plan. Then those trips are passed back to the page.
- searchMap: If the user clicks a pin on the map, a link is displayed to view all trips for that location. When the link is clicked, it passes the location name into this search function to return all trips with that location name present in the location, title, or plan.
- addToList: Allows a user to add a trip to a list of their choosing by passing in the list names and trip id.
- removeFromList: Allows a user to remove a trip from a list.
- edit_trip: Allows a user to edit the photos, title, tags, and plans of a trip they have created.
- all_been: Loads all of the trips with status "been" so that Javascript can access these trips and pin them on the map. 

### models.py
The models created for this web app are:
- User: contains AbstractUser elements plus first name, a profile photo, and the user's home location (all info is entered upon registering and can be updated via edit_profile view)
- Trip: contains the user who created the trip(FK:User), trip title, location, timestamp, budget, plans, status (been or future), and img(this field is JUST the trip's cover photo)
- Tag: contains tag names and a Many To Many Field for all of the trips with that tag name
- List: contains list names, user(FK:User), and a Many to Many Field for all of the trips on that list
- Photo: contains photo, caption, and a FK field for the trip that photo goes with 

### Javascript Files
Javascript files were created for each individual html page since certain elements are only found on certain pages.
- browse.js: If the browse page is displaying trips for a certain list, a "Remove From List" button will be displayed. This file contains javascript to update the display of the button once clicked.
- edit.js: When the user clicks "+ Add New Tag Field" button, a new text input will appear for them to add another tag.
- index.js: Uses Google Maps Platform API to dynamically load a map with markers for each location of all of the trips in the database. Adds info boxes to each marker and when users click the marker the box pops up with a link to view all trips at this location. 
- lists.js: If the user clicks "+ Create New List", a new text input will appear to type in the name of the new list and save it.
- plan.js: When the user clicks "+ Add New Tag Field" button, a new text input will appear for them to add another tag. Similar to edit.js but the stlye properties of the tag fields are different.
- profile.js: Contains the same function to create a new list as lists.js plus the function to toggle the view of Edit Profile or View Profile. If users click the edit profile button, then the edit profile view is displayed and the regular view is hidden. 
- travel.js: Contains functions to toggle the navigation dropdown menu & to toggle the display of the mobile menu. Also contains the function to allow users to click "Jump to Top" and be taken to the top of the page after scrolling a certain amount. This file is linked in the layout.html page so the functions apply to the site at all times.
- trip.js: Function to toggle "Add to List" view which will cause all of the lists to transition onto the page using animation. Also contains functions to open and close the photos carousel. 

### styles.css
Contains all of the css for the web app to style buttons, links, etc. Also contains css to animate certain elements and to make the site mobile-responsive by changing certain display properties when the screen size is 600px or less.

### Templates
- browse.html: This template displays preview information for all of the trips that are sent to it through views context
- captions.html: This template is displayed after a user plans a trip if they have uploaded photos. It displays the photos with a text input for them to enter captions for each photo.
- edit.html: This template displays information for a single trip within the text inputs and textarea so the user can edit what has already been entered.
- index.html: This template displays a Google Map with markers for all of the locations of the trips in the database. 
- layout.html: This template contains all of the navigation bar elements that are present on every page.
- login.html: This template contains the login form.
- mylists.html: This template displays the lists of the logged in user.
- plan.html: This template displays the form for a user to plan a trip. It includes buttons, text inputs, photo upload fields, and a rich text-editor textarea for the user to enter the information about their trip. 
- profile.html: This template displays a user's profile and all of the trips they've planned.
- register.html: This template displays the register form.
- trip.html: This template displays all the details of a specific trip. 

## Possible Improvements
- I ran into some issues with my sortby/search functions. If the user searches for something, they aren't able to sort their search so I would like to improve these functions so that they are able to sort their search. 
- Actually link the application to user emails by sending a registration confirmation email, allowing for "Forgot My Password" emails, etc.

## How to Run this Application
- Go to [my GitHub repository](https://github.com/ginacostanzo/CS50W-Final.git).
- Click the "Code" button and click the 'Download zip' option.
- Import the files to VS Code or your preferred app on your machine. 
- cd into the top level directory
- In the terminal, enter python3 manage.py runserver
- Click the link
