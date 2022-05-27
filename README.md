# tesedee
&lt;redacted> energy service engineering data engineer evaluation

A simple Flask-based answer to the coding question presented.
## Setup
A supported Python 3 installation is assumed (>= 3.7) along with Git.

### Clone the repo
    git clone git@github.com:bspkrs/tesedee.git
    cd tesedee

### Install Flask in a virtual environment
#### Bash
    python3 -m venv venv
    . venv/bin/activate
    pip install Flask
#### Windows CMD
    py -3 -m venv venv
    venv\Scripts\activate
    pip install Flask

## Execution
### Bash
    cd src/python
    export FLASK_APP=first_pass.py
    flask run
     * Running on http://127.0.0.1:5000/'
### Windows CMD
    cd src\python
    set FLASK_APP=first_pass.py
    flask run
     * Running on http://127.0.0.1:5000/

## Sending test requests
### Bash
    curl -i http://127.0.0.1:5000/temp -X POST -H 'Content-Type: application/json' -d '{"data":"365951380:1640995229697:'\''Temperature'\'':58.48256793121914"}'
    curl -i http://127.0.0.1:5000/temp -X POST -H 'Content-Type: application/json' -d '{"data":"365951380:1640995229697:'\''Temperature'\'':158.48256793121914"}'
    curl -i http://127.0.0.1:5000/temp -X POST -H 'Content-Type: application/json' -d '{"data":"NotAnInt:1640995229697:'\''Temperature'\'':58.48256793121914"}'
    curl -i http://127.0.0.1:5000/temp -X POST -H 'Content-Type: application/json' -d '{"data":"365951380:NotAnInt:'\''Temperature'\'':58.48256793121914"}'
    curl -i http://127.0.0.1:5000/temp -X POST -H 'Content-Type: application/json' -d '{"data":"365951380:1640995229697:'Temperature':58.48256793121914"}'
    curl -i http://127.0.0.1:5000/temp -X POST -H 'Content-Type: application/json' -d '{"data":"365951380:1640995229697:'\''Temperature'\'':NotAFloat"}'
    curl -i http://127.0.0.1:5000/errors -X GET
    curl -i http://127.0.0.1:5000/errors -X DELETE
### Windows Powershell
I honestly tried to get Invoke-WebRequest working for this... MS just HAD to be different 
from curl... you're better off installing Cygwin or the Windows Linux Subsystem to use 
curl and just run the command above.

## A note about complexity and the delivered solution
Admittedly I didn't put as much time into this as I wanted to be able to. Due to many 
factors (timing mostly) I decided to start with a very basic bare-bones implementation 
of the solution that met the minimum criteria outlined in the problem statement, but I 
also intended to create a shinier version of the solution that used better practices and 
followed trusted design patterns for RESTful web services; however, due to life and work 
and time spent interviewing and not working on this, I didn't get as far as I wanted with 
that shinier solution. As a result the code I am submitting is not something that I am 
super-proud of and the ugliness of it is almost embarrassing to me.

I realize that you can't give me marks based on the work of others, but for what it's 
worth, the better version was to be modeled after the concepts outlined in this Flask(+) 
example project: https://github.com/apryor6/flask_api_example
I wish as much as you do that circumstances had been better and I had been able to 
produce a prettier implementation with more extensible practices employed.

Either way, thanks for your consideration!  
-bspkrs
