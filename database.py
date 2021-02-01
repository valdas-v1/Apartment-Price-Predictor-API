import psycopg2
from sqlalchemy import create_engine
import os
import io
import pandas as pd

class Database:
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