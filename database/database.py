import os
import psycopg2
import psycopg2.extras
import logging
logger = logging.getLogger(__name__)

class Database:

    def __init__(self):
        self.dbname = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.schema_name = os.getenv("DB_SCHEMA")
        self.conn = self.connect()

    def get_connection(self):        
        if self.conn is None or self.conn.closed == 1:
            self.conn = self.connect()

        return self.conn

    def connect(self):
        try:
            return psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port, options=f"-c search_path={self.schema_name},public")
        except psycopg2.Error as e:
            logger.error("Error connecting to database:", e)
            exit()

    def insert(self, query, params):
        logger.debug(f"Running insert: {query} - {params}")
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)
        conn.commit()
        cursor.close()

    def update(self, query, params):
        logger.debug(f"Running update: {query} - {params}")
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)
        conn.commit()
        cursor.close()

    def select_all(self, query):
        logger.debug(f"Running select: {query}")
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(query)

        result = cursor.fetchall()

        if result:
            return result
        else:
            return None
        
    def select_all_dict(self, query):
        logger.debug(f"Running select: {query}")
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute(query)

        result = cursor.fetchall()

        if result:
            return [dict(row) for row in result]
        else:
            return None

    def select(self, query, params=None):
        logger.debug(f"Running select: {query} - {params}")
        conn = self.get_connection()
        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        result = cursor.fetchone()

        if result:
            return result
        else:
            return None
