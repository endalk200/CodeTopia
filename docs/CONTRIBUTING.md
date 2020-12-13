# Contributing to this project

> The world can only really be changed one piece at a time.  The art is picking that piece.
>
> &mdash; [Tim Berners-Lee][cite]

This documentations goal is to make contributing to this project as easy as possible for you. We hope you will have pleasent experience in participating on this project.

A good first start is to start a discussion either by joining our [Telegram Group](https://t.me/CodeTopia) or through [Github Discussions](https://github.com/EthiOpenSource/CodeTopia/discussions). Since this idea and project is not developed yet you can contribute by giving some ideas and thoughts on the project through the above means. 

The most important thing you can do to help push this project forward is to be actively involved wherever possible. You can tell your friends about this project and help them to find this project, The more people know about the idea the better it gets. 

## Types of Contributions

### Code Contribution

You can contribute code to this repository. Since it is a new project there is a lot to be done. Not sure what to do use the [Telegram Group](https://t.me/CodeTopia) or  [Github Discussions](https://github.com/EthiOpenSource/CodeTopia/discussions) to get in touch.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "feature" is open to whoever wants to implement it.

### Write Documentation

This Project could always use more documentation, whether as part of the official docs, in docstrings.

### Submit Feedback
 
The best way to send feedback is through [Telegram Group](https://t.me/CodeTopia) or  [Github Discussions](https://github.com/EthiOpenSource/CodeTopia/discussions).

If you are proposing a feature:

* Explain in detail how it would work.
* Remember that this is a volunteer-driven project, and that contributions are welcome :)



## Development

To start developing, `fork` the repo and clone it locally:

* **Install dependencies**

There are two main components of this project the frontend and the backend. <br>
To install the frontend dependencies:

    cd frontend/
    npm install

To install backend dependecies:

    cd backend/
    # Create a virtualenvironment
    virtualenv env
    # Activate the environment
    source env/bin/activate
    pip install -r requirements.txt

* **Run tests locally**

To run the tests in the backend:

    cd backend/
    python manage.py test
    flake8

* **Run the web application**

To run the backend server:

    cd backend/
    python manage.py runserver

To run the frontend use a new terminal:

    cd frontend/
    npm start

> **NOTE:** If you have trouble cloning the repo or runing it locally you can either open an issue or as for help on either the  [Telegram Group](https://t.me/CodeTopia) or [Github Discussions](https://github.com/EthiOpenSource/CodeTopia/discussions). 
>>If you had problem with runing it locally but fixed by yourself or find this getting started guide misleading or lack something please improve the documentation and open a pull request.

# **Thank You**