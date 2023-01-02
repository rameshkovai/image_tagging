import mysql.connector


class MysqlConnector:
    """
    This method acts as a connector to get data from MySQL
    """
    def __init__(self, username, password, host, database):
        self.connection_params = {
            'user': username,
            'password': password,
            'host': host,
            'database': database
        }
        self.db_conn = mysql.connector.connect(**self.connection_params)

    def get_cursor(self, dict_cursor=True):
        """
        This method is called to get the cursor object
        :param dict_cursor: dict cursor will be requested when user needs a dict response
        :return: cursor object
        """
        return self.db_conn.cursor(dictionary=dict_cursor)

    def process_query(self, query, args=None, get_primary_key=False):
        """
        This method is called to process the query and return the results
        :param query: MySQL query
        :param args: arguments to the query
        :param get_primary_key: get primary key is called to store the primary key information to database
        :return: result of the query
        """
        curs = self.get_cursor()
        curs.execute(query, args)
        if get_primary_key:
            return curs.lastrowid
        result = curs.fetchall()
        return result

    def commit(self):
        """
        This method is called to commit the transaction
        """
        self.db_conn.commit()

    def close(self):
        """
        This method is called to close the connection created
        """
        self.db_conn.close()


if __name__ == "__main__":  # pragma: no cover
    mysql_conn = MysqlConnector('root', 'Global!23', 'localhost', 'document_management')
    query_result = mysql_conn.process_query("select * from user")
    mysql_conn.commit()
    mysql_conn.close()

