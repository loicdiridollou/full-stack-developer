import psycopg2

conn = psycopg2.connect('dbname=example user=joe password=test')

cursor = conn.cursor()


cursor.execute("SELECT * FROM table2;")

result = cursor.fetchall()
print(result)

conn.commit()

conn.close()
cursor.close()