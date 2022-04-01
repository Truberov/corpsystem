import os

from starlette.config import Config


dir_path = os.path.dirname(os.path.realpath(__file__))
root_dir = dir_path[:-3]
config = Config(f'{root_dir}.env')

DATABASE_URL = f'sqlite:///{root_dir}' + config('DB_NAME', cast=str)


jwt_secret = config('JWT_SECRET', cast=str)
jwt_algorithm: str = 'HS256'
jwt_expiration: int = 3600
