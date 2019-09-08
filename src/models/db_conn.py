from mysql import connector
from config.config import get_config
sql_conn = connector.connect(
    user=get_config('mysql', 'username'),
    passwd=get_config('mysql', 'password'),
    host=get_config('mysql', 'sql_host'),
    database=get_config('mysql', 'database'),
    port=get_config('mysql', 'port')
)
cursor = sql_conn.cursor(buffered=True)