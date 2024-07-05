# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone https://github.com/KseniaLysikova/mtuciPractice.git
    $ cd mtuciPractice/parsingApp
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Start the system with docker-compose up.

    $ docker-compose up

Go to http://localhost:8000/ to use the form to parse data.
Go to http://localhost:8000/result/ to watch parsed data and filter it if necessary.

# Starting tests

    $ docker-compose run django python manage.py test
