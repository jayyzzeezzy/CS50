# Work Order
#### Video Demo:  <https://youtu.be/YvIvkoaTCys>

## Welcome!

My name is James Zhou and this is my CS50 final project: *Work Order*.

### Description

Work Order is a Web App that aims to facilitate the maintenance process at individual's apartment home, by allowing the tenants and maintenace team to schedule dates and communicate with each other virtually. To begin, you'll need to register for an account. After registration, you'll be redirected to the `maintenance` page, where you can submit a maintenance request.  You may also message the maintenance team by using the `message` page. This web app was created using languages such as Python, HTML, CSS, JavaScript, and SQL. Frameworks that were used to create this project include but are not limited to Flask and Django.


## Navigating the Page
* Register
* Log In/Out
* Homepage
* Maintenance
* Status
* Message
* Inbox
* Sent

### Register

When you click on the `Register` tab, you will be taken to the registration page where you can create your account by choosing a unique username and password, and specifying your role as either a tenant or contractor. In case the username you desire is already taken, an error message will appear on the next page, informing you that the username already exists.

### Log In/Out

Upon accessing Work Order, you will be directed to the `Login` page, where you can enter your registered username and password. If the information you provide matches with the records we have on file, you will be granted access to the website.

### Homepage

After successfully logging in, you will be directed to the `Homepage`, where you can access detailed information about all your work order requests. Here, you will find information such as work order ID, apartment number, scheduled service date and time, and status of completion. The requests are also separated by their completion status, with all completed requests displayed at the bottom of the page and all recent pending and dispatching requests at the top.

### Maintenance

New users will be automatically redirected to the `Maintenance` page after successfully creating an account. Users can access this page by clicking on the `Maintenance` tab on the navigation bar. On this page, you can provide the maintenance team with your contact information, report any issues you are experiencing, and specify your preferred date and time for the team to visit. This information will help the maintenance team efficiently address your requests and provide you with the necessary assistance.

### Status

On the `Status` page, you can easily update the status of your work order request. By default, the status is set to *Pending*. To update the status, you can simply click on the drop down menu and mark it as *Dispatched worker* or *Completed*. Once a work order is marked as *Completed*, it will automatically appear at the bottom of your Homepage.


### Message

If you have any questions about your request, you can click on the `Message` tab in order to send a message. Once you access this page, you'll be asked to fill out a form for your message. The form will ask for your username, the recipient's username, subject and body of your message, and details of your work order. If you need to send a message exclusively to the maintenance team, set the recipient to <contractor@cs50workorder.com>.

### Inbox

The `Inbox` page is where you can view any messages you receive. To see details about a message, simply click the `View Message` button. Then you will be redirected to the `View` page. On this page, you can read the message and choose to reply by clicking the `Reply` button.

### Sent

This page shows any *outgoing* messages you may have. The `Sent` page will display each individual message in a list format and you can see message details by clicking on the `View Message` button.


## Closing Remarks

I would like to express my gratitude to [David Malan](https://cs.harvard.edu/malan/) and the entire [CS50](https://cs50.harvard.edu/x/2023/) team for creating an exceptional course. I started this course with no knowledge on the field, but I knew programming has always sparked my interest. David's teaching style and his passion for teaching made this class an enjoyable experience. He was very thorough at explaining at every step of the way and really go indepth about why programers do certain things and what are the conventional methods in the world of programming. At the end of the class, I was able to approach problems by thinking more computationally. Moving forward, I would like to continue to learn more about programming and pursue a career in the software engineering space. Feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/jzfromkp/) or Discord `@JZfromKP#6237`.

Thank you for checking out *Work Order*. This was CS50!