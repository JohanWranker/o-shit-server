from flask import Flask, jsonify, request
from flask import render_template


app = Flask(__name__)

toilets = [
    {
        "name": "Toilet",
        "location": [30, 100],
        "status": "free",
    },
    {
        "name": "Toilet2",
        "location": [200, 200],
        "status": "free",
    },
]


def occupy_toilet(name):
    for toilet in toilets:
        if toilet["name"] == name:
            toilet["status"] = "occupied"
            print(f"Toilet {name} is now occupied")
            return jsonify(toilet)
    return jsonify({"error": "Toilet not found"}), 404


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.png")


@app.route("/clicked_toilet", methods=["GET"])
def clicked_toilet():
    name = request.args.get("name")
    for toilet in toilets:
        if toilet["name"] == name:
            occupy_toilet(name)
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
                                fetch(`/clicked_toilet?name=${toilet.name}`);
                                fetch('/toilets_positions')
                                    .then(response => response.json())
                                    .then(data => {
                                        data.data.forEach(updatedToilet => {
                                            if (updatedToilet.name === toilet.name) {
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


if __name__ == "__main__":
    app.run(debug=True)
