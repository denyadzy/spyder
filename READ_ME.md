You sould have python, Git, pip on your compter
https://pip.pypa.io/en/stable/installing/

https://git-scm.com/book/ru/v1/%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5-%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-Git

https://www.python.org/downloads/


Before installing and lounching spider you shold intall virtualenv in terminal:

$ sudo pip install virtualenv

and louch virtualenv  from terminal:

$ virtualenv ENV

Where ENV is a directory to place the new virtual environment.
Then activate it:

$ source bin/activate

download all files from github :

$ git clone https://github.com/denyadzy/spyder.git

Install all requirements from file requirements.txt with command in terminal:

$ pip install -r requirements.txt

Go to the folder ip_port in terminal and lounch spider:

$ scrapy crawl port_spider










