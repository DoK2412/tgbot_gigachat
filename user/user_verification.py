from database.connection import JobDb
import database.scheme as schem

from datetime import datetime


class User(object):

    __user = dict()

    def __init__(self,
                 id=None,
                 name=None,
                 active=None,
                 creation_date=None,
                 blocking_date=None,
                 requests=None,
                 language=None):
        self.id = id
        self.name = name
        self.active = active
        self.creation_date = creation_date
        self.blocking_date = blocking_date
        self.requests = requests
        self.language = language

    @classmethod
    async def get_user(cls, data):
        users = await User.getting_user(data.chat.id)
        if users is not None:
            return await User.user_return(users)
        else:
            await User.creating_user(data)
            users = await User.getting_user(data.chat.id)
            return await User.user_return(users)

    @classmethod
    async def creating_user(cls, data):
        date = datetime.now()
        async with JobDb() as connector:
            await connector.execute(schem.ADD_USER, data.chat.username, data.chat.id, date)

    @classmethod
    async def getting_user(cls, id):
        async with JobDb() as connector:
            users = await connector.fetchrow(schem.CHECK_USER, id)
            return users

    @classmethod
    async def user_return(cls, users):
        if users['user_id_telegram'] in cls.__user:
            return cls.__user[users['user_id_telegram']]
        else:
            cls.__user[users['user_id_telegram']] = User(id=users['user_id_telegram'],
                    name=users['user_name'],
                    active=users['active'],
                    creation_date=users['creation_date'],
                    blocking_date=users['blocking_date'],
                    requests=users['requests'],
                    language=None)
            return cls.__user[users['user_id_telegram']]


