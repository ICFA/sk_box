import shlex
import subprocess
from flask import Flask

app = Flask(__name__)


@app.route("/uptime", methods=["GET"])
def uptime():
    command = shlex.split(f"uptime")
    UPTIME = subprocess.run(command, capture_output=True)
    return f"Current uptime is {UPTIME}"


if __name__ == "__main__":
    app.run(debug=True)