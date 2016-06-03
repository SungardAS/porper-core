
class User:

    def __init__(self, connection):
        self.connection = connection

    def create(self, params):
        sql = "INSERT INTO users (id, email, family_name, given_name, name) VALUES ('" + params['id'] + "', '" + params['email'] + "', '" + params['family_name'] + "', '" + params['given_name'] + "', '" + params['given_name'] + " " + params['family_name'] + "')"
        print sql
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        self.connection.commit()

    def find(self, params):
        sql = "SELECT * FROM users"
        if params.get('role_id'):
            sql += " WHERE id IN (SELECT user_id FROM users_roles WHERE role_id = '" + params['role_id'] + "')"
        elif params.get('role_ids'):
            sql += " WHERE id IN (SELECT user_id FROM users_roles WHERE role_id IN ('" + "','".join(params['role_ids']) + "'))"
        elif params.get('ids'):
            sql += " WHERE id IN ('" + "','".join(params['ids']) + "')"
        elif params.get('ids') == [] or params.get('role_ids') == []:
            sql += " WHERE 1 = 0"
        elif params.get('id'):
            sql += " WHERE id = '" + params['id'] + "'"
        print sql
        rows = []
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            for row in cursor:
                rows.append({'id':row[0], 'email':row[1], 'family_name':row[2], 'given_name':row[3], 'name':row[4]})
        self.connection.commit()
        return rows
