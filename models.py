import datetime
from peewee import *
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

DATABASE = SqliteDatabase('quotes')
# DATABASE = PostgresqlDatabase('quotes', user='mattadmin', password='password')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        email = email.lower()
        try:
            cls.select().where(
                (cls.email==email)
            ).get()
        except cls.DoesNotExist:
            user = cls(username=username, email=email)
            user.password = generate_password_hash(password)
            user.save()
            return user
        else:
            raise Exception("user with that email already exists ya dingus!!")



class Quote(Model):
    body = CharField()
    attributed_to = CharField()
    medium = CharField()
    created_by = ForeignKeyField(User, related_name='quote_set')
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Quote], safe=True)
    DATABASE.close()