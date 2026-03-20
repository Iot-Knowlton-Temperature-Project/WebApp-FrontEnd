from flask import Flask, jsonify, make_response, render_template
from sql_manager import query_sensor_statuses
from datetime import datetime

app = Flask(__name__)

def get_data():
    statuses = query_sensor_statuses(timeout_seconds=15)
    return (
        statuses.get(1, "Unknown"),
        statuses.get(2, "Unknown"),
        statuses.get(3, "Unknown"),
        statuses.get(4, "Unknown"),
        statuses.get(5, "Unknown"),
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
    return jsonify({
        "sense1_status": statuses.get(1, "Unknown")[0],
        "sense1_last_seen": statuses.get(1, "Unknown")[1],
        "sense1_temp": statuses.get(1, "Unknown")[2],
        "sense1_hum": statuses.get(1, "Unknown")[3],

        "sense2_status": statuses.get(2, "Unknown")[0],
        "sense2_last_seen": statuses.get(2, "Unknown")[1],
        "sense2_temp": statuses.get(2, "Unknown")[2],
        "sense2_hum": statuses.get(2, "Unknown")[3],
        
        "sense3_status": statuses.get(3, "Unknown")[0],
        "sense3_last_seen": statuses.get(3, "Unknown")[1],
        "sense3_temp": statuses.get(3, "Unknown")[2],
        "sense3_hum": statuses.get(3, "Unknown")[3],
        
        "sense4_status": statuses.get(4, "Unknown")[0],
        "sense4_last_seen": statuses.get(4, "Unknown")[1],
        "sense4_temp": statuses.get(4, "Unknown")[2],
        "sense4_hum": statuses.get(4, "Unknown")[3],
        
        "sense5_status": statuses.get(5, "Unknown")[0],
        "sense5_last_seen": statuses.get(5, "Unknown")[1],
        "sense5_temp": statuses.get(5, "Unknown")[2],
        "sense5_hum": statuses.get(5, "Unknown")[3],

        "checked_at": datetime.now().isoformat(timespec="seconds"),
    })

if __name__ == '__main__':
    app.run(debug=True)