from flask import Flask, request, jsonify
import logging
import os, json
from time import sleep

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='log.log',
                    filemode='w')
logging.debug('A debug message')
logging.info('Some information')
logging.warning('A shot across the bows')


# 192.168.0.193

app = Flask(__name__)

data_file = "data.json"
with open(data_file, 'r') as infile:
    data = json.load(infile)

presets_file = "presets.json"
with open(presets_file, 'r') as infile:
    presets = json.load(infile)


# ---------VOLUME CONTROLS--------- #

# single press up
@app.route("/vol_up_one", methods=["GET"])
def vol_up_one():
    print("irsend SEND_ONCE AMP vol_up")
    return "volume up one"

# single press down
@app.route("/vol_down_one", methods=["GET"])
def vol_down_one():
    print("irsend SEND_ONCE AMP vol_down")
    return "volume down one"

# held press up start
@app.route("/vol_up_start", methods=["GET"])
def vol_up_start():
    print("irsend SEND_START AMP vol_up")
    return "start turning up volume"

# held press up stop
@app.route("/vol_up_stop", methods=["GET"])
def vol_up_stop():
    print("irsend SEND_STOP AMP vol_up")
    return "stop turning up volume"

# held press down start
@app.route("/vol_down_start", methods=["GET"])
def vol_down_start():
    print("irsend SEND_START AMP vol_down")
    return "start turning down volume"

# held press down stop
@app.route("/vol_down_stop", methods=["GET"])
def vol_down_stop():
    print("irsend SEND_STOP AMP vol_down")
    return "stop turning down volume"


# ---------CHOOSE ACTIVITY--------- #
@app.route("/activity/<choice>", methods=["GET"])
def select_activity(choice):
    selected_activity = presets[choice]
    # iterate through every setting in the selected activity
    for i in selected_activity:
        for y in selected_activity[i]:
            # if there is a difference between the current
            # system state and the selected activity state
            if data[i][y] != selected_activity[i][y]:
                # then change the current state
                data[i][y] = selected_activity[i][y]
                # and run the command
                if y == "app":
                    print("adb shell input keyevent 3")
                    print(selected_activity[i][y])                        
                else:
                    print("irsend SEND_ONCE %s %s" % (i, selected_activity[i][y]))
                    sleep(2)

    # write the system state changes back out to json
    with open(data_file, 'w') as outfile:
        json.dump(data, outfile)
    return jsonify(data)

# ---------SELECT CHANNEL--------- #
@app.route("/channel/<number>", methods=["GET"])
def select_channel(number):
    for i in str(number):
        input_number = "input_" + i
        print("irsend SEND_ONCE UPC %s" % input_number)
        print("irsend SEND_ONCE UPC down")
        sleep(.3)
    print("irsend SEND_ONCE UPC up")
    return "channel selected " + number

@app.route("/nav/<remote_input>", methods=["GET"])
def navigate(remote_input):
    if remote_input == "up":
        print("irsend SEND_ONCE UPC up")
        return "upc input up"

    elif remote_input == "down":
        print("irsend SEND_ONCE UPC down")
        return "upc input down"

    elif remote_input == "left":
        print("irsend SEND_ONCE UPC up")
        print("irsend SEND_ONCE UPC left")
        return "upc input left"

    elif remote_input == "right":
        print("irsend SEND_ONCE UPC up")
        print("irsend SEND_ONCE UPC right")
        return "upc input right"

    elif remote_input == "ok":
        print("irsend SEND_ONCE UPC ok")
        return "upc input ok"

    elif remote_input == "back":
        print("irsend SEND_ONCE UPC back")
        return "upc input back"
        
    else:
        return "incorrect input"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)