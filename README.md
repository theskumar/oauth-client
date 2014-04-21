OAuth Client
============

What is this?
-------------

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iste, vitae, praesentium eligendi temporibus in molestias excepturi nesciunt fuga natus laborum minus ab quas corrupti est fugit ipsam maxime facere. Rem.

Instructions
------------

First, you'll need to clone the repo.

    $ git clone git@github.com:theskumar/oauth-client.git
    $ cd oauth-client

Second, let's download `pip`, `virtualenv`, `foreman`, and the [`heroku`
Ruby gem](http://devcenter.heroku.com/articles/using-the-cli).

    $ sudo easy_install pip
    $ sudo pip install virtualenv
    $ sudo gem install foreman heroku

Now, you can setup an isolated environment with `virtualenv`.

    $ virtualenv --no-site-packages venv
    $ source venv/bin/activate

Then, let's get the requirements installed in your isolated test
environment.

    $ pip install -r requirements.txt


Running Your Application
------------------------

Now, you can run the application locally.

    $ foreman start

You can also specify what port you'd prefer to use.

    $ foreman start -p 5555


Deploying
---------

If you haven't [signed up for Heroku](https://api.heroku.com/signup), go
ahead and do that. You should then be able to [add your SSH key to
Heroku](http://devcenter.heroku.com/articles/quickstart), and also
`heroku login` from the commandline.

Now, to upload your application, you'll first need to do the
following -- and obviously change `app_name` to the name of your
application:

    $ heroku create app_name -s cedar

And, then you can push your application up to Heroku.

    $ git push heroku master
    $ heroku scale web=1

Finally, we can make sure the application is up and running.

    $ heroku ps

Set up some required variables:

    $ heroku config:set SECRET=<random_secret>

At join.agiliq.com, register your application and get the `client_id` and `client_secret` and add `<yourdomain>/callback/agiliq` as redirect url. 


    $ heroku config:set AGILIG_CLIENT_ID=<your agiliq client id>
    $ heroku config:set AGILIG_CLIENT_SECRET=<your agiliq client secret>

Now, we can view the application in our web browser.

    $ heroku open

And, to deactivate `virtualenv` (once you've finished coding), you
simply run the following command:

    $ deactivate


Reactivating the Virtual Environment
------------------------------------

If you haven't worked with `virtualenv` before, you'll need to
reactivate the environment everytime you close or reload your terminal.

    $ source env/bin/activate

If you don't reactivate the environment, then you'll probably receive a
screen full of errors when trying to run the application locally.

License
--------
Copyright 2014 Saurabh Kumar

