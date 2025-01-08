import sqlite3

class SQLite():
    def __init__(self, database_name):
        self.database_name = database_name
        self.conn = self.connect_database()
        self.create_user_table()
        self.create_query_table()
    
    def connect_database(self):
        return sqlite3.connect(self.database_name)
    
    def create_user_table(self):
        query = f"""
                CREATE TABLE IF NOT EXISTS user(
                username TEXT,
                password TEXT,
                email TEXT,
                role TEXT
                )
                """
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
    
    def create_query_table(self):
        query = f"""
                CREATE TABLE IF NOT EXISTS query(
                prompt TEXT
                )
                """
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
    
    def fetch_queries(self):
        query = f"""
                SELECT * from query
                """
        cursor = self.conn.cursor()
        prompts = cursor.fetchall()
        self.conn.commit()
        if prompts:
            return [prompt for prompt in prompts]
    
    def update_queries(self, queries_list):
        print(queries_list)
        query = f"""
                DROP TABLE IF EXISTS query
                """
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        self.create_query_table()
        insert_query = f"""
                        INSERT INTO query (prompt)
                        VALUES (?)
                        """
        # for query in queries_list:
        #     cursor.execute(insert_query, query)
        cursor.executemany(insert_query, queries_list)
        self.conn.commit()

    def fetch_users(self):
        query = f"""
                SELECT * from user
                """
        cursor = self.conn.cursor()
        cursor.execute(query)
        users = cursor.fetchall()
        self.conn.commit()
        if users:
            return [user for user in users]
        
    def fetch_user(self, username, password):
        query = f"""
                SELECT * FROM user WHERE username = '{username}' and password = '{password}'
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        user = cursor.fetchone()
        self.conn.commit()
        return user

    
    def create_user(self, username, password, email, role):
        user = self.fetch_user(username, password)
        if user is None:
            query = f"""
                    INSERT INTO user (username, password, email, role)
                    VALUES ('{username}', '{password}', '{email}', '{role}')
                    """
            cursor = self.conn.cursor()
            cursor.execute(query)
            result = self.fetch_user(username, password)
            self.conn.commit()
            if result is not None:
                return result
        return None
    
    def authenticate_user(self, username, password):
        user = self.fetch_user(username, password)
        if user is not None:
            return user
        
    def update_user_role(self, username, role):
        cur = self.conn.cursor()
        query = f"""
                UPDATE user
                SET role = '{role}'
                WHERE username = '{username}'
                """
        cur.execute(query)
        self.conn.commit()
        ## Verify role is updated or not
        query = f""" 
                SELECT * FROM user WHERE username = '{username}' AND role = '{role}'
                """ 
        cur.execute(query) 
        result = cur.fetchone()
        self.conn.commit()
        return result
    
    def delete_user(self, username):
        query = f"""
                DELETE FROM user
                WHERE username = '{username}'
                """
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        ## Verify role is updated or not
        query = f""" 
                SELECT * FROM user WHERE username = '{username}'
                """ 
        cursor.execute(query) 
        result = cursor.fetchone()
        self.conn.commit()
        return result  