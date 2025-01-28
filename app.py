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
        "location": [200, 1000],
    },
]


@app.route("/toilets_positions")
def toilets_positions():
    return jsonify([toilets])


@app.route("/click_location", methods=["POST"])
def click_location():
    x = request.form.get("x")
    y = request.form.get("y")
    for toilet in toilets:
        if (
            toilet["location"][0] <= int(x) <= toilet["location"][0] + 10
            and toilet["location"][1] <= int(y) <= toilet["location"][1] + 10
        ):
            print("Click is on the toilet")
            break
    else:
        print("Click is not on the toilet")
    # Process the click location as needed
    print(f"Click location received: x={x}, y={y}")
    return f"Click location received: x={x}, y={y}"


""""""


""" <script>
                document.getElementById('toilet').style.left = `${toilet.location[0]}px`;
                document.getElementById('toilet').style.top = `${toilet.location[1]}px`;
            </script>"""


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
                        data.forEach(d => {
                        d.forEach(toilet => {
                            console.log(toilet);
                            var x = toilet.location[0];
                            var y = toilet.location[1];
                            var toiletDiv = document.createElement('div');
                            toiletDiv.style.position = 'absolute';
                            toiletDiv.style.left = `${x}px`;
                            toiletDiv.style.top = `${y}px`;
                            toiletDiv.style.width = '10px';
                            toiletDiv.style.height = '10px';
                            toiletDiv.style.backgroundColor = 'red';
                            toiletDiv.style.borderRadius = '50%';
                            document.body.appendChild(toiletDiv);
                            console.log("Image size: width=" + x + ", height=" + y);
                        });
 });
                    });
            </script>
        </body>
    </html>    
    """


if __name__ == "__main__":
    app.run(debug=True)
