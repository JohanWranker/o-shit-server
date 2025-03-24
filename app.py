from flask import Flask, jsonify, request
from flask import render_template
import datetime


app = Flask(__name__)

toilets = [
    {
        "id": 1, #IVSS
        "location": [112, 90],
        "status": "free",
    },
     {
        "id": 2, #IVSS
        "location": [112, 100],
        "status": "free",
    },
    {
        "id": 3, #IVSS
        "location": [121, 90],
        "status": "free",
    },
     {
        "id": 4, #IVSS
        "location": [121, 100],
        "status": "free",
    },
     {
        "id": 60, #stareway
        "location": [169, 81-7*2],
        "status": "free",
    },
     {
        "id": 60, #stareway
        "location": [169, 81-7],
        "status": "free",
    },
     {
        "id": 60, #stareway
        "location": [169, 81],
        "status": "free",
    },



     {
        "id": 5, #copy
        "location": [130, 100],
        "status": "free",
    },
    {
        "id": 10, #small kitchen
        "location": [90, 326],
        "status": "free",
    },
     {
        "id": 11, #small kitchen
        "location": [90, 333],
        "status": "free",
    },
    {
        "id": 12, #small kitchen
        "location": [90, 340],
        "status": "free",
    },
     {
        "id": 13, #small kitchen
        "location": [90, 347],
        "status": "free",
    },
    {
        "id": 50, #E
        "location": [97, 355],
        "status": "free",
    },
     {
        "id": 51, #E
        "location": [105, 355],
        "status": "free",
    },
    




    {
        "id": 20, #bigexit
        "location": [85, 485],
        "status": "free",
    },
    {
        "id": 21, #bigexit
        "location": [85-7, 485],
        "status": "free",
    },
    {
        "id": 22, #bigexit
        "location": [85-7*2, 485],
        "status": "free",
    },
    {
        "id": 23, #bigexit
        "location": [85-7*3, 485],
        "status": "free",
    },
    {
        "id": 24, #bigexit
        "location": [85-7*4, 490],
        "status": "free",
    },
    {
        "id": 30, #bigexit
        "location": [125, 503],
        "status": "free",
    },
    {
        "id": 30, #bigexit
        "location": [125, 510],
        "status": "free",
    },
    
]

status_db = {}
for toilet in toilets:
    status_db[toilet["id"]] = {}

@app.route("/book_toilet", methods=["GET"])
def book_toilet():
    toilet_id = request.args.get("toilet_id")
    time = request.args.get("time")
    name = request.args.get("name")

    if not toilet_id or not time or not name:
        return jsonify({"error": "Missing parameters"}), 400
    try:
        toilet_id = int(toilet_id)
    except ValueError:
        return jsonify({"error": "Invalid toilet ID"}), 400
    if toilet_id not in status_db:
        return jsonify({"error": "Toilet not found"}), 404
    try:
        booking_time = datetime.datetime.strptime(f"{datetime.datetime.now().strftime('%Y-%m-%d')}T{time}:00", "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return jsonify({"error": "Invalid time format"}), 400
    
    if booking_time in status_db[toilet_id]:
        return jsonify({"error": "Time slot is already occupied"}), 400

    status_db[toilet_id][time] = name

    return jsonify({"message": "Toilet booked successfully"}, 200)


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
            <img id="layoutImg" src="/static/o2.jpg" alt="o2 layout" onclick="sendClickLocation(event)">
            <script>
                // Adjust body width to match the image's rendered width
                window.addEventListener('load', function() {
                    const layoutImg = document.getElementById('layoutImg');
                    document.body.style.width = layoutImg.width + 'px';
                });

                fetch('/toilets_positions')
                    .then(response => response.json())
                    .then(data => {
                        data.data.forEach(toilet => {
                            var toiletDiv = document.createElement('div');
                            toiletDiv.style.position = 'absolute';
                            toiletDiv.style.left = `${toilet.location[0]}px`;
                            toiletDiv.style.top = `${toilet.location[1]}px`;
                            toiletDiv.style.width = '7px';
                            toiletDiv.style.height = '7px';
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
                                window.location.href = `/time_slots_table?id=${toilet.id}`;
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
    toilet_id = request.args.get("id","")
    table_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h2>Time Slots for Toilet {toilet_id}</h2>
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
                                row.addEventListener('click', function() {
                                    if (!isOccupied) {
                                        window.location.href = `/booking_page?toilet_id={toilet_id}&time=${slotTimeStr}`;
                                    } else {
                                        alert('This time slot is already occupied');    
                                    }
                                });
                                
                            });
                        });
                });
        </script>
    </body>
    </html>
    """.replace("{toilet_id}", toilet_id)
    return table_html




@app.route("/booking_page")
def booking_page():
    toilet_id = request.args.get("toilet_id","")
    time = request.args.get("time","")
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h2>Booking Confirmation</h2>
        <p>Are you sure you want to book Toilet {toilet_id} at {time}?</p>
        <input type="text" id="name" name="name" placeholder="name" onfocus="this.placeholder = ''" onblur="this.placeholder = 'name'">
        <button onclick="bookToilet()">Book</button>
        <button onclick="window.history.back()">Cancel</button>
        <script>
            function bookToilet() {
                const name = document.getElementById('name').value;
                if (!name) {
                    alert('Please enter your name');
                    return;
                }
                fetch(`/book_toilet?toilet_id={toilet_id}&time={time}&name=${name}`)
                    .then(response => response.json())
                    .then(data => {
                        alert('Toilet booked successfully');
                        window.location.href = '/';
                    });
            }
        </script>
    </body>
    </html>
    """.replace("{toilet_id}", toilet_id).replace("{time}", time)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
