# MEMORIALIST
#### Video Demo:  <[URL HERE](https://youtu.be/23uFh-g_GjE)>
#### Description:
This project is created to help users with learning foreign languages. I've recently moved to Germany. And it is hard for me to memorise a lot of new words. So using this project I can create my user, add cards with specific words and it's translation. And then I can go through all the cards to memorise them.

In this project I used Flask, python, html, scc, java-script and SQL.

Below there is a description of a project structure.

There is app.py file, with which I can basically run project and navigate through the pages. Here you could find all the routes and see it's behavior. Some routs have only GET method, but most of them have both GET and POST methods. This is the main file that put all pieces all together. There is also helper.py file where helper functions are located. For different routers I needed to use the same pieces of code, such as 'Login required' and 'Database connection'. So it was better to initialize them as helper functions.

There is a Template folder that contains a list of .html files, that represent different pages or the project. 
1. index.html page is the main one. User gets here from the start.
2. register.html page is for ability to create a user. So every person can create their own base of cards that are stored for him/her specifically.
3. login.html page is for logging in to the project. It allows to store users session and use it on other pages.
4. dashboard.html page is the overview of logged user. So it gives a look of a base of existing cards for this specific user. And it also allows to create new cards.
5. study.html page is opening a mode, where user could go through all the existing cards, flip it back and forth to see the translation. There is also an arrow button to go to the next card. The cards are shown in random order. There is also a counter to see how many cards are left till the end of one set. And there is a checkbox for 'learned' cards, so user could mark it and it won't be shown in next sets.
6. There is also layout.html file, that helps to have the same layout at all pages and not repeat it everytime.

There is also card.db file with database to store created cards for specific user. This database is updated every time when user added card and when he/she marks the card as 'learned'
And there is the init_db.py file that helps to use this db in the app.

There is also Static folder, that contains Images folder with all needed images for the project. And there is a styles.css file, that stores all the information about style of the project.

