import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Config class
    """

    POSTGRES = {
        'database': os.getenv('POSTGRES_NAME'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('POSTGRES_PORT'),
    }

    RABBIT = {
        'host': os.getenv('RABBIT_MQ_HOST'),
        'port': int(os.getenv('RABBIT_MQ_PORT')),
        'username': os.getenv('RABBIT_MQ_USER'),
        'password': os.getenv('RABBIT_MQ_PASSWORD')
    }

    WEBSOCKET_PORT = int(os.getenv('WEBSOCKET_PORT'))

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '[%(asctime)s][%(threadName)s] %(funcName)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'simple',
                'stream': 'ext://sys.stdout'
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False
            },
        }
    }
