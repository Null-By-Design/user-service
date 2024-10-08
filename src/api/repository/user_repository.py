import psycopg2

from src.api.config.__init__ import settings


def get_db_connection():
    """
    Establishes a connection to the database, using the DATABASE_URL environment
    variable or the default setting for the current environment.

    Returns a psycopg2 connection object.
    """
    return psycopg2.connect(settings.DATABASE_URL)


def check_db_connection():
    """
    Attempts to establish a connection to the database and execute a simple
    query.

    Returns a string indicating the outcome of the check. If the check
    succeeds, the string will be "Connected". If the check fails, the
    string will be a description of the error that occurred.

    :return: A string indicating the health of the database connection.
    :rtype: str
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return "Connected"
    except Exception as e:
        return f"Failed to connect to database: {e}"
