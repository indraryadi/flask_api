import yaml
import psycopg2
from psycopg2.extras import RealDictCursor


def connection():
  location = 'config.yaml'
  with open(location) as file:
    config = yaml.safe_load(file)
    config = config['postgresql']

  try:
    connection = psycopg2.connect(
    host=config['host'],
    user=config['user'],
    password=config['password'],
    database=config['database'],
    port=config['port']
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)
  except Exception as e:
    raise e

  return connection, cursor
