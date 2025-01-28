from flask import Flask, jsonify, request
from flask import render_template


app = Flask(__name__)

toilets = [
    {
        "name": "Toilet",
        "location": [30, 100],
    },
    {
        "name": "Toilet2",
        "location": [200, 200],
    },
]


@app.route("/toilets_positions")
def toilets_positions():
    return jsonify(data=toilets)


@app.route("/click_location", methods=["POST"])
def click_location():
    toiletname = request.form.get("toiletname")
    print("Click is on the toilet:", toiletname)
    return jsonify(success=True)


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.png")


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
        <body style="overflow: scroll;">
            <img src="/static/image.jpg" alt="Sample Image" onclick="sendClickLocation(event)">
            
           
           
            <script>
                function sendClickLocation(event) {
                    var x = event.clientX;
                    var y = event.clientY;
                    var img = document.querySelector('img');
                    var imgWidth = img.clientWidth;
                    var imgHeight = img.clientHeight;
                    console.log("Image size: width=" + imgWidth + ", height=" + imgHeight);
                    var xhr = new XMLHttpRequest();
                    xhr.open("POST", "/click_location", true);
                    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                    xhr.send("x=" + x + "&y=" + y);
                }
            </script>
           
            <script>
                fetch('/toilets_positions')
                    .then(response => response.json())
                    .then(data => {
                        console.log(data); // `data` is now a JavaScript object
                        data.data.forEach(toilet => {
                            toiletIndex = data.data.indexOf(toilet);
                            console.log(toilet);
                            var x = toilet.location[0];
                            var y = toilet.location[1];
                            var toiletDiv = document.createElement('div');
                            toiletDiv.style.position = 'absolute';
                            toiletDiv.style.left = `${x}px`;
                            toiletDiv.style.top = `${y}px`;
                            toiletDiv.style.width = '50px';
                            toiletDiv.style.height = '50px';
                            toiletDiv.style.backgroundColor = 'red';
                            toiletDiv.style.borderRadius = '50%';
                            toiletDiv.toiletname = toilet.name;
                            document.body.appendChild(toiletDiv);
                            console.log("Image size: width=" + x + ", height=" + y);
                            toiletDiv.addEventListener('click', function(event) {
                                var xhr = new XMLHttpRequest();
                                xhr.open("POST", "/click_location", true);
                                xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                                xhr.send("x=" + x + "&y=" + y + "&toiletname=" + toilet.name);
                            });
                        });
                    });
            </script>
        </body>
    </html>    
    """


if __name__ == "__main__":
    app.run(debug=True)
