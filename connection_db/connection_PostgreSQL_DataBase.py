from peewee import *
import json

with open("config.json", "r") as read_file:
    data = json.load(read_file)


db = PostgresqlDatabase(
    data["db_name"],
    user=data["user"],
    password=data["password"],
    host=data["host"],
    port=data["port"]
)
