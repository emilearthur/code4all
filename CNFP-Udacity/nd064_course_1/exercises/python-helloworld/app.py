from flask import Flask
import json
import logging

app = Flask(__name__)

@app.route("/")
def hello():
    app.logger.info("Main request successfull")
    return "Hello World!"

@app.route("/status")
def healthcheck():
    response = app.response_class(response=json.dumps("result: Ok - healthy"),
                                  status=200,
                                  mimetype='application/json')
    app.logger.info("Status request successful")  # log status
    # return "result:Ok - healthy"
    return response

@app.route("/metrics")
def metrics():
    response = app.response_class(response=json.dumps({"status": "status", "code":0, "data":{"UserCount": 140, "UserCountActive": 23}}),
                                  status=200,
                                  mimetype='application/json')
    app.logger.info("Metrics request successfull")  # log metrics
    # return "data: {UserCount: 140, UserCountActive: 23}"
    return response


if __name__ == "__main__":
    # stream logs to app.log file
    logging.basicConfig(filename='app.log', level=logging.DEBUG)
    app.run(host='0.0.0.0', debug=True)
