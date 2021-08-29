System dependencies
-------------------

This project use python3 and postgresql. You need to install and configure some
system package to get ready.

   | sudo apt-get install postgresql libpq-dev
   | sudo apt-get install python3-dev python3-venv

Be sure that your system user can list and create database.
Try to run :

   psql -l

If it fails, you need to create a postgresql user. For that you need to became
the postgres user

   | sudo -u postgres bash
   | createuser --interactive
   | exit

You should now be able to run `psql -l` with your account

You need to create a .env file containing following data to set up the project configuration::

   DB_USERNAME="username"
   DB_PASSWORD="password"
   DB_ADDRESS="address of the database"
   DB_NAME="name of the dabatase"
