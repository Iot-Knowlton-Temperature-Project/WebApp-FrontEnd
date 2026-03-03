#!/usr/bin/python3

import urllib.parse
import os
import html
import mariadb
import sys
import time

print("Content-type: text/html\n")

try:
	raw_len = os.environ.get("CONTENT_LENGTH") or "0"
	try:
		content_length = int(raw_len)
	except:
		content_length = 0

	#content_length = int(os.environ.get("CONTENT_LENGTH, 0")
	post_data = sys.stdin.read(content_length)
	params = urllib.parse.parse_qs(post_data)
	temp = float(params.get("temp", [0])[0])
	hum = float(params.get("hum", [0])[0])
	sensor_id = int(params.get("sensor_id", [0])[0])

	if sensor_id != 0:
		conn = mariadb.connect (
			user="root",
			password="changeme",
			host="localhost",
			database="esp"
		)
		cur = conn.cursor()
		cur.execute("INSERT INTO weather (sensor_id, date_time, temperature, humidity) VALUES (?, NOW(), ?, ?);",
				(sensor_id, temp, hum)
		)
		conn.commit()
		conn.close()
		print("<p>Data Received and Stored</p>")

except Exception as e:
	print(f"Error: {e}")

print("<html>")
print("<head><title>ESP Weather Page</title></head>")
print("<body>")
print("<h1>ESP Weather Page</h1>")


try:
	conn = mariadb.connect (
		host='localhost',
		user='root',
		password='changeme',
		database='esp'
	)
	cur = conn.cursor()
	cur.execute('SELECT * FROM weather ORDER BY id DESC;')
	row = cur.fetchone()
	if row:
		print(f"<p>Entry ID: {row[0]}</p>") 
		print(f"<p>Sensor ID: {row[1]}</p>")
		print(f"<p>Temperature: {row[3]:.2f} F</p>")
		print(f"<p>Humidity: {row[4]:.2f}%</p>")
		print(f"<p>Time: {row[2]}</p>")
	else:
		print("<p>No data found.</p>")

except mariadb.Error as e :
	print(f"<p>Database Error! {e}</p>")

print("</body>")
print("</html>")





