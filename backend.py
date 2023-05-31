# from django.db.backends.sqlite3.base import DatabaseWrapper as Sqlite3DatabaseWrapper
# import sqlite3
#
# from jsonfield import json
#
#
# class JSONFieldSqlite3DatabaseWrapper(Sqlite3DatabaseWrapper):
#     def get_new_connection(self, conn_params):
#         conn = super().get_new_connection(conn_params)
#         conn.create_function("json_extract", 2, _json_extract)
#         return conn
#
#
# def _json_extract(json_string, key):
#     json_dict = json.loads(json_string)
#     return json_dict.get(key)