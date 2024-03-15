from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Event:
    db_name = "anton_db"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.location = data['location']
        self.date = data['date']
        self.event_time = data['event_time']
        self.price = data['price']
        self.image_upload = data['image_upload']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def deleteComment(cls, data):
        query = "DELETE FROM comments where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def get_comment_by_id(cls, data):
        query = 'SELECT * FROM comments where id = %(id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False

    @classmethod
    def get_event_by_id(cls, data):
        query = 'SELECT * FROM events left join users on events.user_id = users.id where events.id = %(event_id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            query2 = 'SELECT * FROM comments left join users on comments.user_id = users.id WHERE comments.event_id = %(event_id)s;'
            results2 =  connectToMySQL(cls.db_name).query_db(query2, data)
            comments = []
            if results2:
                for comment in results2:
                    comments.append(comment)
            result[0]['comments'] = comments
            return result[0]
        return False
        
    @classmethod
    def addComment(cls, data):
        query = "INSERT INTO comments (komenti, user_id, event_id) VALUES (%(komenti)s, %(user_id)s, %(event_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def addTicket(cls, data):
        query = "INSERT INTO billets (full_name, email, telephone_number, number_tickets, event_title, user_id) VALUES (%(full_name)s, %(email)s, %(telephone_number)s, %(number_tickets)s, %(event_title)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    

    @classmethod
    def create(cls, data):
        query = "INSERT INTO events (title, description, location, date, price, image_upload, event_time, user_id) VALUES (%(title)s, %(description)s, %(location)s, %(date)s, %(price)s, %(image_path)s, %(event_time)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
     

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM events;"
        results = connectToMySQL(cls.db_name).query_db(query)
        events = []
        if results:
            for event in results:
                events.append(event)
        return events

    @classmethod
    def get_event_by_creator(cls):
        query = "SELECT * FROM events LEFT JOIN users on events.user_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        events = []
        if results:
            for event in results:
                events.append(event)
        return events

    @classmethod
    def get_one_event_with_creator(cls, data):
        query = "SELECT * FROM events LEFT JOIN users on events.user_id = users.id WHERE events.id= %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def geteventsByCreator(cls, data):
        query = "SELECT * FROM events LEFT JOIN users on events.user_id = users.id WHERE users.id= %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results
        return False
    
    @classmethod
    def deletePostComments(cls,data):
        query = "DELETE FROM comments where comments.event_id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM events where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE events set description = %(description)s WHERE events.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_event(data):
        is_valid = True
        if len(data['title'])< 2:
            flash('Title should be more  or equal to 2 characters', 'title')
        # if data['title'] == data['title']:
        #   flash('Title should be unique', 'valideTitleUnique')
        #   is_valid = False
        if len(data['description'])< 10:
            flash('Description should be more  or equal to 10 characters', 'description')
            is_valid = False
        return is_valid
    
    @classmethod
    def addLike(cls, data):
        query = "INSERT INTO subscribers (user_id, event_id) VALUES (%(user_id)s, %(event_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def removeLike(cls, data):
        query = "DELETE FROM subscribers WHERE event_id=%(event_id)s AND user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_users_who_liked_by_book_id(cls, data):
        query ="SELECT user_id FROM subscribers where event_id = %(event_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        usersId = []
        if results:
            for userId in results:
                usersId.append(userId['user_id'])
        return usersId
                
