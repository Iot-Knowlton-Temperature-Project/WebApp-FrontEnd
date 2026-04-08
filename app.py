

# Actual Temperature: ~70.2
# Sensor 1: ~72.24 : Error: +2.04
# Sensor 2: ~71.41 : Error: +1.21
# Sensor 3: ~72.44 : Error: +2.24
# Sensor 4: ~71.78 : Error: +1.58
# Sensor 5: ~71.05 : Error: +0.85



from flask import Flask, jsonify, make_response, render_template
from sql_manager import query_sensor_statuses
from datetime import datetime

app = Flask(__name__)
DEFAULT_STATUS = ("Unknown", "0", "0", "0")

def get_data():
    statuses = query_sensor_statuses(timeout_seconds=15)
    return (
        statuses.get(1, DEFAULT_STATUS),
        statuses.get(2, DEFAULT_STATUS),
        statuses.get(3, DEFAULT_STATUS),
        statuses.get(4, DEFAULT_STATUS),
        statuses.get(5, DEFAULT_STATUS),
    )

@app.route("/")
def hello_world():
    sense1_status, sense2_status, sense3_status, sense4_status, sense5_status = get_data()
    response = make_response(render_template(
        'index.html',
        sense1_status=sense1_status[0],
        sense1_last_seen=sense1_status[1],
        sense1_temp=sense1_status[2],
        sense1_hum=sense1_status[3],

        sense2_status=sense2_status[0],
        sense2_last_seen=sense2_status[1],
        sense2_temp=sense2_status[2],
        sense2_hum=sense2_status[3],

        sense3_status=sense3_status[0],
        sense3_last_seen=sense3_status[1],
        sense3_temp=sense3_status[2],
        sense3_hum=sense3_status[3],

        sense4_status=sense4_status[0],
        sense4_last_seen=sense4_status[1],
        sense4_temp=sense4_status[2],
        sense4_hum=sense4_status[3],

        sense5_status=sense5_status[0],
        sense5_last_seen=sense5_status[1],
        sense5_temp=sense5_status[2],
        sense5_hum=sense5_status[3]
    ))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/data")
def data():
    return render_template('data.html')


@app.route("/api/status")
def api_status():
    statuses = query_sensor_statuses(timeout_seconds=15)
    s1 = statuses.get(1, DEFAULT_STATUS)
    s2 = statuses.get(2, DEFAULT_STATUS)
    s3 = statuses.get(3, DEFAULT_STATUS)
    s4 = statuses.get(4, DEFAULT_STATUS)
    s5 = statuses.get(5, DEFAULT_STATUS)

    response = jsonify({
        "sense1_status": s1[0],
        "sense1_last_seen": s1[1],
        "sense1_temp": s1[2],
        "sense1_hum": s1[3],

        "sense2_status": s2[0],
        "sense2_last_seen": s2[1],
        "sense2_temp": s2[2],
        "sense2_hum": s2[3],

        "sense3_status": s3[0],
        "sense3_last_seen": s3[1],
        "sense3_temp": s3[2],
        "sense3_hum": s3[3],

        "sense4_status": s4[0],
        "sense4_last_seen": s4[1],
        "sense4_temp": s4[2],
        "sense4_hum": s4[3],

        "sense5_status": s5[0],
        "sense5_last_seen": s5[1],
        "sense5_temp": s5[2],
        "sense5_hum": s5[3],

        "checked_at": datetime.now().isoformat(timespec="seconds"),
    })
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == '__main__':
    app.run(debug=True)