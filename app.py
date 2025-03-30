from flask import Flask, jsonify, request
from flask import render_template
import datetime


app = Flask(__name__)

toilets = [
    {
        "id": 1, #IVSS
        "location": [112 * 4.1, 190],
    },
     {
        "id": 2, #IVSS
        "location": [112 * 4.1, 215],
    },
    {
        "id": 3, #IVSS
        "location": [121 * 4.1, 190],

    },
     {
        "id": 4, #IVSS
        "location": [121 * 4.1, 215],

    },
     {
        "id": 5, #copy
        "location": [130 * 4.1, 215],

    },
     {
        "id": 60, #stareway
        "location": [780, (95-7*2) * 1.72],

    },
     {
        "id": 61, #stareway
        "location": [780, (95-7) * 1.72],

    },
     {
        "id": 62, #stareway
        "location": [780, 95 * 1.72],

    },
    {
        "id": 63, #stareway
        "location": [780, (95-7*3-5) * 1.72],

    },
    {
        "id": 64, #stareway
        "location": [830, (95-7*3-5) * 1.72],

    },



    
    {
        "id": 10, #small kitchen
        "location": [90 * 4.1, 326 * 1.72],

    },
     {
        "id": 11, #small kitchen
        "location": [90 * 4.1, 333 * 1.72],

    },
    {
        "id": 12, #small kitchen
        "location": [90 * 4.1, 340 * 1.72],

    },
     {
        "id": 13, #small kitchen
        "location": [90 * 4.1, 347 * 1.72],

    },
    {
        "id": 50, #E
        "location": [330, 575],

    },
     {
        "id": 51, #E
        "location": [330, 590],

    },
    




    {
        "id": 20, #bigexit
        "location": [85 * 4.1+15, 485 * 1.72],

    },
    {
        "id": 21, #bigexit
        "location": [85 * 4.1 - 7*4.1+15, 485 * 1.72],

    },
    {
        "id": 22, #bigexit
        "location": [85 * 4.1 - 7*4.1*2+15, 485 * 1.72],

    },
    {
        "id": 23, #bigexit
        "location": [85 * 4.1 - 7*4.1*3+15, 485 * 1.72],

    },
    {
        "id": 24, #bigexit
        "location": [85 * 4.1 - 7*4.1 * 4+15, 490 * 1.72],

    },
    {
        "id": 30, #classic
        "location": [125 * 4.1+15, 503 * 1.72],

    },
    {
        "id": 31, #classic
        "location": [125 * 4.1+15, 510 * 1.72],

    },
    {
        "id": 31, #classic
        "location": [125 * 4.1-15, 510 * 1.72-30],

    },
    {
        "id": 31, #classic
        "location": [125 * 4.1+15, 510 * 1.72-30],

    },
    
]

statistics = {
    "start_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "qr_code_read": 0,
    "viewed": 0,
    "bookings": 0,
}
status_db = {}
for toilet in toilets:
    status_db[toilet["id"]] = {}



@app.route("/book_toilet", methods=["GET"])
def book_toilet():
    toilet_id = request.args.get("toilet_id")
    time = request.args.get("time")
    name = request.args.get("name", "")
    unbook = request.args.get("unbook")
    ip = request.remote_addr
   
    if not toilet_id or not time or not (name or unbook):
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
    
    if unbook:
        if booking_time not in status_db[toilet_id]:
            return jsonify({"error": "Time slot is not occupied"}), 400
        if status_db[toilet_id][booking_time][1] != ip:
            return jsonify({"error": "You cannot un-book this toilet"}), 403
        del status_db[toilet_id][booking_time]
        return jsonify({"message": "Toilet un-booked successfully"}, 200)
    
    #Book
    if booking_time in status_db[toilet_id]:
        return jsonify({"error": "Time slot is already occupied"}), 400

    status_db[toilet_id][booking_time] = [name, ip]

    return jsonify({"message": "Toilet booked successfully"}, 200)



@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.png")

@app.route("/toilets_positions", methods=["GET"])
def toilets_positions():
    for toilet in toilets:
        for time, _ in status_db[toilet["id"]].items():
            # Check if the time is within the next 5 minutes
            low = datetime.datetime.now() - datetime.timedelta(minutes=4, seconds=59)
            high = datetime.datetime.now() + datetime.timedelta(minutes=5)
            if low < time and time < high:
                # If the toilet is booked, set its status to "occupied"
                toilet["status"] = "occupied"
                break
        else:
            toilet["status"] = "free"
    return jsonify(data=toilets)

@app.route("/qr")
def qr():
    statistics["qr_code_read"] += 1
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="0;url=/" />
    </head>
    <body>
        <p>If you are not redirected automatically, follow this <a href="/">link</a>.</p>
    </body>
    </html>
    """


@app.route("/")
def splash():
    return """
    <!DOCTYPE html>
        <head>
            <link rel="stylesheet" href="/static/style.css">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="refresh" content="2;url=/home">
        </head>
        <body>
            <h1>Welcome to the O2 Toilet Booking System</h1>
            <button onclick="window.location.href='/home'">Go to Booking Page Now</button>
        </body>
    </html>
    """

@app.route("/home")
def home():
    statistics["viewed"] += 1
    return """
    <!DOCTYPE html>
        <head>
            <link rel="stylesheet" href="/static/style.css">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="overflow: scroll;">
            <img id="layoutImg" src="/static/o2.jpg" alt="o2 layout" onclick="sendClickLocation(event)" style="width: 100%; height: auto;">
            <script>
                fetch('/toilets_positions')
                    .then(response => response.json())
                    .then(data => {
                        const layoutImg = document.getElementById('layoutImg');
                        const imgWidth = layoutImg.offsetWidth;
                        const imgHeight = layoutImg.offsetHeight;

                        data.data.forEach(toilet => {
                            var toiletDiv = document.createElement('div');
                            toiletDiv.style.position = 'absolute';
                            toiletDiv.style.left = `${(toilet.location[0] / 1000) * imgWidth}px`;
                            toiletDiv.style.top = `${(toilet.location[1] / 1000) * imgHeight}px`;
                            toiletDiv.style.width = `${imgWidth * 0.035}px`;
                            toiletDiv.style.height = `${imgWidth * 0.035}px`;
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

                window.addEventListener('resize', function() {
                    location.reload();
                });
            </script>
        </body>
    </html>
    """

def time_range():
    start_time = datetime.datetime.strptime(f"{datetime.datetime.now().strftime('%Y-%m-%d')}T08:00:00", "%Y-%m-%dT%H:%M:%S")
    end_time = datetime.datetime.strptime(f"{datetime.datetime.now().strftime('%Y-%m-%d')}T23:55:00", "%Y-%m-%dT%H:%M:%S")# T15:55:00", "%Y-%m-%dT%H:%M:%S")
    return (start_time, end_time)

@app.route("/office_hours")
def get_time_scope():
    office_hours = {
        "start": time_range()[0],
        "end":time_range()[1],
        "interval": 5,
    }
    return jsonify(office_hours)



@app.route("/toilet_status")
def get_toilet_schedule():
    toilet_id = request.args.get("toilet")
    if not toilet_id:
        return jsonify({"error": "Missing toilet ID"}), 400
    try:
        toilet_id = int(toilet_id)
    except ValueError:
        return jsonify({"error": "Invalid toilet ID"}), 400
    if toilet_id not in status_db:
        return jsonify({"error": "Toilet not found"}), 404
    

    (time, end_time) = time_range()
    
    schedule = []
    while time < end_time:
        short_time = time.strftime('%H:%M')
        booking =  status_db[toilet_id].get(time, {})
        
        
        item = {
            "start": short_time,
            "name": ""
        }
        if booking:
            item["name"] = booking[0]
            item["ip"] = booking[1]
            item["status"] = "Occupied"
        else:
            item["status"] = "Available"
        schedule.append(item)
        time += datetime.timedelta(minutes=5)

    return jsonify(schedule)


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
                    fetch('/toilet_status?toilet={toilet_id}')
                        .then(r => r.json())
                        .then(bookedTimes => {
                            bookedTimes.forEach(slot => {
                                const time = slot.start;
                                const isOccupied = slot.status === "Occupied";
                                const row = document.createElement('tr');
                                const timeTd = document.createElement('td');
                                const statusTd = document.createElement('td');
                                timeTd.textContent = time;
                                statusTd.textContent = isOccupied ? slot.name : 'Available';
                                statusTd.className = isOccupied ? 'occupied' : 'available';
                                

                                row.appendChild(timeTd);
                                row.appendChild(statusTd);
                                table.appendChild(row);
                                row.addEventListener('click', function() {
                                    if (!isOccupied) {
                                        window.location.href = `/booking_page?toilet_id={toilet_id}&time=${time}`;
                                    } else {
                                        data = `/book_toilet?toilet_id={toilet_id}&time=${time}&unbook=yes`;
                                        fetch(data)
                                            .then(response => response.json())
                                            .then(data => {
                                                if (data[1] !== 200) {
                                                    alert(data.error);
                                                }
                                                else {
                                                    alert(data[0].message);
                                                }
                                                window.location.reload();
                                            });
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
                fetch(`/book_toilet?toilet_id={toilet_id}&time={time}&name=${encodeURIComponent(name)}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data[1] !== 200) {
                            alert(data.error);
                        }
                        else {
                            alert(data[0].message);
                        }
                        window.location.href = '/home';

                    });
            }
        </script>
    </body>
    </html>
    """.replace("{toilet_id}", toilet_id).replace("{time}", time)


@app.route("/about")
def about():
    data ="""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>About</h1>
        <p>I hope that you liked my first of April program</p>
        <p>best regards Johan Wranker</p>
        <p>Version 1.0</p>
        <p>Statistics:</p>
        <ul>
            <li>QR code scanned: {qr_code_read}</li>
            <li>Page viewed: {viewed}</li>
            <li>Bookings made: {bookings}</li>
            <li>Start time: {start_time}</li>
    </body>
    </html>
    """
    data = data.replace("{qr_code_read}", str(statistics["qr_code_read"]))
    data = data.replace("{viewed}", str(statistics["viewed"]))
    data = data.replace("{bookings}", str(statistics["bookings"]))
    data = data.replace("{start_time}", statistics["start_time"])
    return data



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
