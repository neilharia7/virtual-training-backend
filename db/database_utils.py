import traceback

import pymysql

from config.settings import current_config as conf


def create_db_connection():
	"""
	
	:return:
	"""
	return pymysql.connect(conf.DATABASE_SERVER, conf.USERNAME, conf.PASSWORD, conf.DATABASE_NAME)


def initiate_query(query):
	"""
	
	:param query:
	:return:
	"""
	conn = create_db_connection()
	print("connection established")
	print(query)
	cur = conn.cursor(pymysql.cursors.DictCursor)
	
	response = dict()
	try:
		cur.execute(query=query)
		print(f"row count >> {cur.rowcount}")
		
		response['success'] = True
		response['data'] = cur.fetchone() if cur.rowcount == 1 else cur.fetchall()
		
		return response
	except Exception as e:
		print(f"query exception {e}")
		traceback.print_exc()
		raise Exception(f"{e}")
	
	finally:
		conn.commit()
		cur.close()
		conn.close()
