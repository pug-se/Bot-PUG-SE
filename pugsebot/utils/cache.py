import datetime
import peewee
from playhouse.db_url import connect
from .environment import DATABASE_URL
from .logging import cache_logger

_db = connect(DATABASE_URL)

class Cache(peewee.Model):
    key = peewee.CharField(unique=True)
    result = peewee.TextField(null=False)
    expire_time = peewee.DateTimeField(null=False)

    class Meta:
        database = _db

    @classmethod
    def set_value(cls, key, result, expire):
        expire_time = datetime.datetime.now()
        expire_time += datetime.timedelta(seconds=expire)
        try:
            cached_item = cls.get(cls.key == key)
            cached_item.result = result
            cached_item.expire_time = expire_time
            cached_item.save()
        except:
            cached_item = cls.create(
                key=key, result=result,
                expire_time=expire_time,
            )
        return cached_item

    @classmethod
    def get_value(cls, key):
        now = datetime.datetime.now()
        try:
            cached_result = cls.get(
                (cls.key == key) &\
                (cls.expire_time > now)
            )
            cache_logger.info(
                f'Hit for key: {key}'\
                f' and expire_time: {cached_result.expire_time}'
            )
            return cached_result
        except:
            return None

_db.connect()
_db.create_tables([Cache])
