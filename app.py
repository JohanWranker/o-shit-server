from flask import Flask, jsonify, request
from flask import render_template


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


@app.route("/tt")
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


@app.route("/time")
def time_picker():
    available_times = [
        {"start": "08:00", "end": "09:00"},
        {"start": "10:00", "end": "12:00"},
        {"start": "13:00", "end": "16:00"},
    ]

    occupied_times = [
        {"start": "09:00", "end": "10:00"},
        {"start": "12:00", "end": "13:00"},
    ]

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/flatpickr/4.6.9/flatpickr.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/flatpickr/4.6.9/flatpickr.min.js"></script>
    </head>
    <body>
        <input type="text" id="timePicker" placeholder="Select Time">
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                flatpickr("#timePicker", {
                    enableTime: true,
                    noCalendar: true,
                    dateFormat: "H:i",
                    time_24hr: true,
                    minuteIncrement: 10,
                    minTime: "08:00",
                    maxTime: "16:00",
                    disable: [
                        {from: "09:00", to: "10:00"},
                        {from: "12:00", to: "13:00"}
                    ]
                });

                const availableTimes = ${json.dumps(available_times)};
                const occupiedTimes = ${json.dumps(occupied_times)};

                const availableList = document.createElement('ul');
                availableList.innerHTML = '<h3>Available Times</h3>';
                availableTimes.forEach(time => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `${time.start} - ${time.end}`;
                    availableList.appendChild(listItem);
                });
                document.body.appendChild(availableList);

                const occupiedList = document.createElement('ul');
                occupiedList.innerHTML = '<h3>Occupied Times</h3>';
                occupiedTimes.forEach(time => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `${time.start} - ${time.end}`;
                    occupiedList.appendChild(listItem);
                });
                document.body.appendChild(occupiedList);
            });
        </script>
    </body>
    </html>
    """


available_times = [
    {"start": "08:00", "end": "09:00"},
    {"start": "10:00", "end": "12:00"},
    {"start": "13:00", "end": "16:00"},
]

occupied_times = [
    {"start": "09:00", "end": "10:00"},
    {"start": "12:00", "end": "13:00"},
]


@app.route("/available_times")
def get_available_times():
    return jsonify(available_times)


@app.route("/occupied_times")
def get_occupied_times():
    return jsonify(occupied_times)


@app.route("/")
def time_picker2():
    available_times = [
        {"start": "08:00", "end": "09:00"},
        {"start": "10:00", "end": "12:00"},
        {"start": "13:00", "end": "16:00"},
    ]

    occupied_times = [
        {"start": "09:00", "end": "10:00"},
        {"start": "12:00", "end": "13:00"},
    ]

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/flatpickr/4.6.9/flatpickr.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/flatpickr/4.6.9/flatpickr.min.js"></script>
        <style>
            .occupied {
                background-color: red !important;
            }
            .available {
                background-color: green !important;
            }
        </style>
    </head>
    <body>
        <input type="text" id="timePicker" placeholder="Select Time">
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                flatpickr("#timePicker", {
                    enableTime: true,
                    noCalendar: true,
                    dateFormat: "H:i",
                    time_24hr: true,
                    minuteIncrement: 10,
                    minTime: "08:00",
                    maxTime: "16:00",
                    disable: [
                        {from: "09:00", to: "10:00"},
                        {from: "12:00", to: "13:00"}
                    ],
                    onChange: function(selectedDates, dateStr, instance) {
                        alert("Selected time: " + dateStr);
                    }
                });
                fetch('/available_times')
                    .then(response => response.json())
                    .then(data => {
                        const availableList = document.createElement('ul');
                        availableList.innerHTML = '<h3>Available Times</h3>';
                        data.forEach(time => {
                            const listItem = document.createElement('li');
                            listItem.textContent = `${time.start} - ${time.end}`;
                            listItem.classList.add('available');
                            availableList.appendChild(listItem);
                        });
                        document.body.appendChild(availableList);
                    });

                fetch('/occupied_times')
                    .then(response => response.json())
                    .then(data => {
                        const occupiedList = document.createElement('ul');
                        occupiedList.innerHTML = '<h3>Occupied Times</h3>';
                        data.forEach(time => {
                            const listItem = document.createElement('li');
                            listItem.textContent = `${time.start} - ${time.end}`;
                            listItem.classList.add('occupied');
                            occupiedList.appendChild(listItem);
                        });
                        document.body.appendChild(occupiedList);
                    });

                const availableList = document.createElement('ul');
                availableList.innerHTML = '<h3>Available Times</h3>';
                availableTimes.forEach(time => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `${time.start} - ${time.end}`;
                    listItem.classList.add('available');
                    availableList.appendChild(listItem);
                });
                document.body.appendChild(availableList);

                const occupiedList = document.createElement('ul');
                occupiedList.innerHTML = '<h3>Occupied Times</h3>';
                occupiedTimes.forEach(time => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `${time.start} - ${time.end}`;
                    listItem.classList.add('occupied');
                    occupiedList.appendChild(listItem);
                });
                document.body.appendChild(occupiedList);
            });
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
