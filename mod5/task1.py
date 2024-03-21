import os
import signal
import subprocess
import shlex
from typing import List
from flask import Flask

app = Flask(__name__)

@app.route("/")
def lsof_site():
    port = 5000
    cmd = f"lsof -i :{port}"
    args = shlex.split(cmd)
    output = subprocess.run(args, capture_output=True)
    resultList = output.stdout.decode().split('\n')[1:-1]
    pidList = []

    for item in resultList:
        pidList.append(int(item.split()[1]))

    if os.getpid() not in pidList:
        for pid in pidList:
            os.kill(pid, signal.SIGKILL)

    return 'Hello!'


if __name__ == '__main__':
    app.run(debug=True, port=5000)