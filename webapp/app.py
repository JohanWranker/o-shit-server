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


@app.route("/toilets_positions")
def toilets_positions():
    return jsonify(data=toilets)


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
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
                                toiletDiv.style.backgroundColor = 'green';
                            } else {
                                toiletDiv.style.backgroundColor = 'red';
                            }
                            toiletDiv.style.borderRadius = '50%';
                            document.body.appendChild(toiletDiv);
                            toiletDiv.addEventListener('click', function(event) {
                                fetch(`/clicked_toilet?id=${toilet.id}`);
                                fetch('/toilets_positions')
                                    .then(response => response.json())
                                    .then(data => {
                                        data.data.forEach(updatedToilet => {
                                            if (updatedToilet.id === toilet.id) {
                                                toiletDiv.style.backgroundColor = updatedToilet.status === 'free' ? 'green' : 'red';
                                            }
                                        });
                                    });
                            });
                            toiletDiv.addEventListener('mouseover', function(event) {
                                toiletDiv.style.transform = 'scale(1.2)';
                            });
                            toiletDiv.addEventListener('mouseout', function(event) {
                                toiletDiv.style.transform = 'scale(1)';
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
    }
    return jsonify(office_hours)


occupied_times = [
    {"start": "09:00", "end": "10:00"},
    {"start": "12:00", "end": "13:00"},
]


@app.route("/occupied_times")
def get_occupied_times():
    return jsonify(occupied_times)


@app.route("/time_slots")
def time_slots():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .occupied {
                background-color: red;
            }
            .available {
                background-color: green;
            }
            .time-slot {
                display: inline-block;
                width: 60px;
                height: 30px;
                margin: 2px;
                text-align: center;
                line-height: 30px;
                border: 1px solid #000;
            }
        </style>
    </head>
    <body>
        <div id="timeSlotsContainer"></div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                fetch('/office_hours')
                    .then(response => response.json())
                    .then(officeHours => {
                        console.log(officeHours);

                        const timeSlotsContainer = document.getElementById('timeSlotsContainer');

                        function generateTimeSlots(start, end, interval) {
                            const slots = [];
                            let current = new Date(officeHours.start);
                            const endDate = new Date(officeHours.end);

                            while (current <= endDate) {
                                slots.push(current.toTimeString().substring(0, 5));
                                current.setMinutes(current.getMinutes() + officeHours.interval);
                            }
                            return slots;
                        }
                 });

                const timeSlots = generateTimeSlots(startTime, endTime, 5);

                fetch('/occupied_times')
                            .then(response => response.json())
                            .then(occupiedTimes => {
                                timeSlots.forEach(slot => {
                                    const slotDiv = document.createElement('div');
                                    slotDiv.classList.add('time-slot');
                                    slotDiv.textContent = slot;

                                    const isOccupied = occupiedTimes.some(time => {
                                        return slot >= time.start && slot < time.end;
                                    });

                                    if (isOccupied) {
                                        slotDiv.classList.add('occupied');
                                    } else {
                                        slotDiv.classList.add('available');
                                    }

                                    timeSlotsContainer.appendChild(slotDiv);
                                });
                            });

                            
            });
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
