from flask import Flask, jsonify, request
from flask import render_template
import datetime


app = Flask(__name__)

toilets = [
    {
        "id": 1,
        "location": [30, 100],
        "status": "free",
    },
    {
        "id": 2,
        "location": [200, 200],
        "status": "free",
    },
]


def occupy_toilet(toilet_id):
    for toilet in toilets:
        if toilet["id"] == toilet_id:
            toilet["status"] = "occupied"
            print(f"Toilet {toilet_id} is now occupied")
            return jsonify(toilet)
    return jsonify({"error": "Toilet not found"}), 404


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.png")


@app.route("/clicked_toilet", methods=["GET"])
def clicked_toilet():
    toilet_id = int(request.args.get("id"))
    for toilet in toilets:
        if toilet["id"] == toilet_id:
            occupy_toilet(toilet_id)
            return jsonify(toilet)
    return jsonify({"error": "Toilet not found"}), 404


@app.route("/toilets_positions", methods=["GET"])
def toilets_positions():
    return jsonify(data=toilets)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
        <head>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body style="overflow: scroll;">
            <img src="/static/image.jpg" alt="Sample Image" onclick="sendClickLocation(event)">
            <script>
                fetch('/toilets_positions')
                    .then(response => response.json())
                    .then(data => {
                        data.data.forEach(toilet => {
                            var toiletDiv = document.createElement('div');
                            toiletDiv.style.position = 'absolute';
                            toiletDiv.style.left = `${toilet.location[0]}px`;
                            toiletDiv.style.top = `${toilet.location[1]}px`;
                            toiletDiv.style.width = '50px';
                            toiletDiv.style.height = '50px';
                            if (toilet.status === 'free') {
                                toiletDiv.className = 'available';
                            } else {
                                toiletDiv.className = 'occupied';
                            }
                            toiletDiv.style.borderRadius = '50%';
                            document.body.appendChild(toiletDiv);
                            
                            toiletDiv.addEventListener('mouseover', function(event) {
                                toiletDiv.style.transform = 'scale(1.2)';
                            });
                            toiletDiv.addEventListener('mouseout', function(event) {
                                toiletDiv.style.transform = 'scale(1)';
                            });
                            toiletDiv.addEventListener('click', function(event) {
                                window.location.href = '/time_slots_table';
                            });
                        });
                    });
            </script>
        </body>
    </html>
    """


@app.route("/office_hours")
def get_time_scope():
    office_hours = {
        "start": f"{datetime.datetime.now().strftime('%Y-%m-%d')}T08:00:00",
        "end": f"{datetime.datetime.now().strftime('%Y-%m-%d')}T15:55:00",
        "interval": 5,
    }
    return jsonify(office_hours)


occupied_times = [
    {
        "start": f"{datetime.datetime.now().strftime('%Y-%m-%d')}T09:00:00",
        "end": f"{datetime.datetime.now().strftime('%Y-%m-%d')}T10:00:00",
    },
    {
        "start": f"{datetime.datetime.now().strftime('%Y-%m-%d')}T12:00:00",
        "end": f"{datetime.datetime.now().strftime('%Y-%m-%d')}T12:10:00",
    },
]


@app.route("/occupied_times")
def get_occupied_times():
    return jsonify(occupied_times)


@app.route("/time_slots_table")
def time_slots_table():
    table_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <table id="timeSlotsTable" border="1" cellpadding="5">
           <tr>
               <th>Time</th>
               <th>Status</th>
           </tr>
        </table>
        <script>
            function generateTimeSlots(startDate, endDate, interval) {
                const slots = [];
                let current = startDate;
                while(current <= endDate) {
                    slots.push(new Date(current));
                    current.setMinutes(current.getMinutes() + interval);
                }
                return slots;
            }
            fetch('/office_hours')
                .then(res => res.json())
                .then(officeHours => {
                    const table = document.getElementById('timeSlotsTable');
                    const timeSlots = generateTimeSlots(new Date(officeHours.start), new Date(officeHours.end), officeHours.interval);
                    fetch('/occupied_times')
                        .then(r => r.json())
                        .then(occupiedTimes => {
                            timeSlots.forEach(slot => {
                                const slotTimeStr = slot.toTimeString().substring(0,5);
                                const isOccupied = occupiedTimes.some(time => {
                                    const startTime = new Date(time.start);
                                    const endTime = new Date(time.end);
                                    return slot >= startTime && slot < endTime;
                                });
                                const row = document.createElement('tr');
                                const timeTd = document.createElement('td');
                                const statusTd = document.createElement('td');
                                timeTd.textContent = slotTimeStr;
                                statusTd.textContent = isOccupied ? 'Occupied' : 'Available';
                                statusTd.className = isOccupied ? 'occupied' : 'available';
                                row.appendChild(timeTd);
                                row.appendChild(statusTd);
                                table.appendChild(row);
                            });
                        });
                });
        </script>
    </body>
    </html>
    """
    return table_html




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
