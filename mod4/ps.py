import shlex
import subprocess
from typing import List
from flask import Flask, request


app = Flask(__name__)

@app.route("/ps/", methods=["GET"])
def _ps():
    args: List[str] = request.args.getlist("args", type=str)
    flag = args[0]
    command = shlex.split(f"ps {flag}")
    result = subprocess.run(command, capture_output=True)
    return f'<pre>{result.stdout.decode()}</pre>'


if __name__ == "__main__":
    app.run(debug=True)