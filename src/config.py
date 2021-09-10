import configparser


# Using configParser instead of dotenv package
# For some reason, load_dotenv couldn't find the
# .env file
config = configparser.ConfigParser()
config.read("config.ini")
