# payana

Set up python3

Set up virtualenv - https://docs.python-guide.org/dev/virtualenvs/

I would recommend to read up all the links and run the Bigtable hello world project first - https://github.com/payanaapp/payana/issues/1

Install flask, read up and work with flask hello world - https://towardsdatascience.com/working-with-apis-using-flask-flask-restplus-and-swagger-ui-7cf447deda7f

Github of the flask hello world -
https://github.com/kb22/Understanding-Flask-and-Flask-RESTPlus

Links to understand flask, flask-restplus and blueprint

https://p5v.medium.com/designing-well-structured-rest-apis-with-flask-restplus-part-1-7e96f2da8850

https://flask-restplus.readthedocs.io/en/stable/scaling.html

#################################################################################################

Fork and clone the Payana git project

Go to payana folder - Find a .env file. If not present create a .env file and add the below variable

travelfont_home="/Users/abhinandankelgereramesh/Documents/payana-github/TravelFont"
Replace the path to your github root TravelFont folder

Source the .env file

Go to payana/payana_service and run -

pip3 install -r requirements.txt

Go to payana/payana_core and run -

pip3 install -r requirements.txt

Then back to payana folder and run -

python setup.py build && python setup.py install

These commands will make Payana available as system python packages to be used for imports

Every time you make any changes to any part of the project run -

python setup.py install --force

This is very important because if you do not run then your changes won’t take effect in the payana package

Also run all this inside a virtualenv because payana is a local package and you don’t want it system wide and also a good coding practice.

Change the config file contents in payana/payana_bl/bigtable_utils/config/client_config.yaml

This config.yaml should contain the Bigtable cluster details of your account. If you have successfully run the hello world Bigtable project you would be aware of the config file content details

Then run payana_bigtable_init.py
