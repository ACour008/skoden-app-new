from flask_sqlalchemy import SQLAlchemy
from flask_cache import Cache

# Database setup
db = SQLAlchemy()

# Cache setup
cache = Cache(config={'CACHE_TYPE': 'simple'})