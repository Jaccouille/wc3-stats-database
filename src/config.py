import configparser


# Using configParser instead of dotenv package
# For some reason, load_dotenv couldn't find the
# .env file
config = configparser.ConfigParser()

# TODO: This currently only works when executing the
# main.py script from the project root directory,
# it's fine for simple usage though
config.read("config.ini")
