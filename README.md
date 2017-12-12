# kitchenin'

Keep your kitchen well-stocked and organized. Kitchenin' helps coordinate your next shopping trip with your house-mates!

I built Kitchenin' primarily to teach myself Django. The idea itself was inspired by numerous daily text-messages and emails asking repeatedly if I needed anything from the store. While I admire and appreciate the sentiment, I knew there was a better way than enduring seemingly endless and inefficient messages.

# Getting started

If you're using Mac OS X, Windows, or a common flavor of Linux these instructions should apply.

1. Clone the repo.

        git clone git@github.com:juli212/kitchenin.git

2. Create a development environment. Python uses [virtual environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to encapsulate the dependencies for a given project. A great tool for managing these environments is [`pyenv`](https://github.com/pyenv/pyenv) and its associated virtual environment manager [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv). *The below assumes that you've installed `pyenv` and `pyenv-virtualenv` using the standard installation instructions.*

        pyenv install 3.6.2
        pyenv virtualenv 3.6.2 kitchen-env
        pyenv activate kitchen-env

3. Install requirements.
       
        pip install -r requirements.txt

    If you have difficulty installing `psycopg2` refer to this stackoverflow question for help: https://stackoverflow.com/questions/28253681/you-need-to-install-postgresql-server-dev-x-y-for-building-a-server-side-extensi.

4. Configure a local [PostgreSQL](https://www.postgresql.org/) database that will be used for development, running tests, etc. If PostgreSQL is not installed on your system, [remedy](https://www.postgresql.org/download/) that (with version 9.5.7 or later). Once PostgreSQL is installed, switch to the system `postgres` user and create the database.

        CREATE USER kitchen_admin;
        ALTER USER kitchen_admin CREATEDB;
        CREATE DATABASE kitchen OWNER kitchen_admin;
        ALTER USER kitchen_admin PASSWORD 'kitchen';

    Leave the `psql` shell, switch back to your standard user and migrate the database.

        python manage.py makemigrations
        python manage.py migrate

# Deployment

Make sure that you have the Heroku remote configured.

    git push heroku master
    heroku run python manage.py migrate

# Appendix

## Further Reading

- [Gunicorn](https://warehouse.python.org/project/gunicorn/)
- [WhiteNoise](https://warehouse.python.org/project/whitenoise/)
- [dj-database-url](https://warehouse.python.org/project/dj-database-url/)
