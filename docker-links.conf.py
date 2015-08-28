postgres = os.getenv('SENTRY_POSTGRES_HOST') or (os.getenv('POSTGRES_PORT_5432_TCP_ADDR') and 'postgres')
mysql = os.getenv('SENTRY_MYSQL_HOST') or (os.getenv('MYSQL_PORT_3306_TCP_ADDR') and 'mysql')
redis = os.getenv('SENTRY_REDIS_HOST') or (os.getenv('REDIS_PORT_6379_TCP_ADDR') and 'redis')
memcached = os.getenv('SENTRY_MEMCACHED_HOST') or (os.getenv('MEMCACHED_PORT_11211_TCP_ADDR') and 'memcached')

if postgres:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': (
                os.getenv('SENTRY_DB_NAME')
                or os.getenv('POSTGRES_ENV_POSTGRES_USER')
                or 'postgres'
            ),
            'USER': (
                os.getenv('SENTRY_DB_USER')
                or os.getenv('POSTGRES_ENV_POSTGRES_USER')
                or 'postgres'
            ),
            'PASSWORD': (
                os.getenv('SENTRY_DB_PASSWORD')
                or os.getenv('POSTGRES_ENV_POSTGRES_PASSWORD')
                or ''
            ),
            'HOST': postgres,
            'PORT': (
                os.getenv('SENTRY_POSTGRES_PORT')
                or ''
            ),
            'OPTIONS': {
                'autocommit': True,
            },
        },
    }
elif mysql:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': (
                os.getenv('SENTRY_DB_NAME')
                or os.getenv('MYSQL_ENV_MYSQL_DATABASE')
                or ''
            ),
            'USER': (
                os.getenv('SENTRY_DB_USER')
                or os.getenv('MYSQL_ENV_MYSQL_USER')
                or 'root'
            ),
            'PASSWORD': (
                os.getenv('SENTRY_DB_PASSWORD')
                or os.getenv('MYSQL_ENV_MYSQL_PASSWORD')
                or os.getenv('MYSQL_ENV_MYSQL_ROOT_PASSWORD')
                or ''
            ),
            'HOST': mysql,
            'PORT': (
                os.getenv('SENTRY_MYSQL_PORT')
                or ''
            ),
        },
    }
else:
    sqlite_path = (
        os.getenv('SENTRY_DB_NAME')
        or 'sentry.db'
    )
    if not os.path.isabs(sqlite_path):
        sqlite_path = os.path.join(CONF_ROOT, sqlite_path)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': sqlite_path,
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        },
    }

if memcached:
    memcached_port = (
        os.getenv('SENTRY_MEMCACHED_PORT')
        or '11211'
    )
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': [memcached + ':' + memcached_port],
        }
    }

if redis:
    redis_port = (
        os.getenv('SENTRY_REDIS_PORT')
        or '6379'
    )
    redis_db = (
        os.getenv('SENTRY_REDIS_DB')
        or '0'
    )
    SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'
    SENTRY_REDIS_OPTIONS = {
        'hosts': {
            0: {
                'host': redis,
                'port': redis_port,
                'db': redis_db,
            },
        },
    }
    BROKER_URL = 'redis://' + redis + ':' + redis_port + '/' + redis_db
else:
    raise Exception('Error: REDIS_PORT_6379_TCP_ADDR (or SENTRY_REDIS_HOST) is undefined, did you forget to `--link` a redis container?')

if SENTRY_URL_PREFIX == 'http://sentry.example.com':
    del SENTRY_URL_PREFIX

if os.getenv('SERVER_EMAIL'):
	SERVER_EMAIL = os.getenv('SERVER_EMAIL')

if os.getenv('EMAIL_HOST'):
	EMAIL_HOST = os.getenv('EMAIL_HOST')

if os.getenv('SENTRY_ADMIN_EMAIL'):
	SENTRY_ADMIN_EMAIL = os.getenv('SENTRY_ADMIN_EMAIL')

if os.getenv('SENTRY_URL_PREFIX'):
	SENTRY_URL_PREFIX = os.getenv('SENTRY_URL_PREFIX')
