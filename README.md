# Pizza-Ordering-Chatbot

## Project URL: http://tiny.cc/dhxwiz
Login credentials:\
  email - nitin@mail.com \
  password - 111
  
### Implemented features
  Created app using, WebSockets, Jinja2, Flask, nltk, threading, tokenizers, regex, javascript, SQLite, flask-migrate, docker, etc.\
  a. Websocket rooms for to and fro conversation between client and server.\
  b. The bot takes in the sentences given by the user, converts the words into their base forms, removes punctuations, removes stop words to get the motive of the user for typing that text. The bot has some given responses for the words after processing. which is returned as a response to the user's chat. There are some functions also added in the chat responses, such as order status and discount coupons.\
  c. On clicking the Order button, the order is inserted into the database and a new thread starts that keeps updating the user after every 10 seconds. The bot delivery status in the thread changes every 10 seconds. 
  d. There are 4 tables:\
        - Menu: Contains the data about Pizza.\
        - User: Contains user's data.\
        - Order: Contains details about user's orders.\
        - Chat: Contains the chats between the user and bot.\
  e. The tables are implemented using flask-sqlalchemy, front-end is done using Jinja2 template. flask-Migrations help in implementing the changes made in the models into the DB through python code and shell commands. Finally, deployed the app on AWS server using docker.
### Yet to be done:
  Some implementations are still pending, some of them are:\
    a. The order status function in the chat response is hard-coded to 'Out for delivery' response.\
    b. More chats need to be implemented, negative responses are not implemented fully.\
    c. Old chat history is not being loaded, need to load chat back from DB.\
    d. Some redirects need to be configured properly.\
    e. Some deployment steps are missing as of now.
