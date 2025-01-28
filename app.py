from flask import Flask, request
from flask import render_template


app = Flask(__name__)

@app.route("/click_location", methods=["POST"])
def click_location():
    x = request.form.get("x")
    y = request.form.get("y")
    # Process the click location as needed
    print(f"Click location received: x={x}, y={y}")
    return f"Click location received: x={x}, y={y}"


@app.route("/")
def home():
    return """
    <html>
        <body>
            <img src="/static/image.jpg" alt="Sample Image" onclick="sendClickLocation(event)">
            <script>
                function sendClickLocation(event) {
                    var x = event.clientX;
                    var y = event.clientY;
                    var xhr = new XMLHttpRequest();
                    xhr.open("POST", "/click_location", true);
                    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                    xhr.send("x=" + x + "&y=" + y);
                }
            </script>
        </body>
    </html>    
    """


if __name__ == "__main__":
    app.run(debug=True)
