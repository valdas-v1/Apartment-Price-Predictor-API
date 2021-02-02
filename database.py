import psycopg2
from sqlalchemy import create_engine
import os
import io
import pandas as pd

class Database:
    """
    Implements saving prediction DataFrames to a remote Heroku postgres database
    """
    def __init__(self):
        # Remote database connection
        self.engine = create_engine(os.environ['HEROKU_DB_24'])
        self.conn = self.engine.raw_connection()
        self.cur = self.conn.cursor()

    def push_dataframe_to_db(self, table_name: str, table_data: pd.DataFrame):

        """
        Uploads the provided DataFrame to the database

        Parameters:
            table_name (str): Name of the table for the data to be added to
            table_data (DataFrame): Data DataFrame to be added to database
        """

        table_data.head(0).to_sql(table_name, self.engine, if_exists='append', index=False)

        output = io.StringIO()
        table_data.to_csv(output, sep='\t', header=False, index=False)
        output.seek(0)
        contents = output.getvalue()
        self.cur.copy_from(output, table_name, null="")
        self.conn.commit()

    def get_requests_and_responses(self, n: int) -> list:

        """
        Return last n most recent requests and responses

        Parameters:
            n (int): The number of requests and responses to query

        Returns:
            query (list): list of last n most recent requests and responses
        """

        self.cur.execute(f'''
        SELECT * FROM predictions LIMIT {n} OFFSET (SELECT count(*) FROM predictions)-{n};
        ''')

        return self.cur.fetchall()