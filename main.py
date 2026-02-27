from __future__ import print_function
from flask import Flask
from flask import request
from flask import render_template
import os
import numpy as np
from scipy import stats
from modeling import model
try:
    import MySQLdb
except ImportError:
    import pymysql as MySQLdb
from flask import session, redirect
from flask import url_for
import re
try:
    import serial
except ImportError:
    serial = None
import time
try:
    import pyttsx as tts_lib
except ImportError:
    try:
        import pyttsx3 as tts_lib
    except ImportError:
        tts_lib = None


# print (model)
app = Flask(__name__)
app.secret_key = "root"
ans = ""


def speak_text(text):
    if tts_lib is None:
        return
    try:
        engine = tts_lib.init()
        engine.say(str(text))
        engine.runAndWait()
    except Exception as exc:
        print("TTS failed:", exc)


def get_available_ports():
    if serial is None:
        return []
    try:
        from serial.tools import list_ports

        return [p.device for p in list_ports.comports()]
    except Exception:
        return []


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/trial', methods=['POST', 'GET'])
def trial():
    ans = request.form['ans']
    session['ans'] = ans
    return render_template("trial.html", ans=ans)


@app.route('/vids', methods=['GET', 'POST'])
def new():
   if request.method=='GET':
    store = (session.get('ans') or "").strip()
    words = store.split() if store else []
    con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="root", db="speech")
    cur = con.cursor()
    a = []
    for i in words:
        # print ("i=",i)
        j = re.sub(r"[^a-z0-9]+", "", str(i).lower())
        if not j:
            continue
        cur.execute('SELECT sign FROM asignl WHERE word= %s', [j])
        data = cur.fetchall()
        # print(data)
        if len(data) < 1:
            continue
        a.append(url_for('static', filename=data[0][0]))
    con.close()

    session['tdata'] = a
    params = a
    textword = store.upper()
    return render_template("vids.html", params=params, words=textword)
   elif request.method == 'POST':
       print ("here")
       return redirect(url_for('index'))


param = []

@app.route('/glove', methods=['GET', 'POST'])
def glove():
    if request.method == 'GET':
        if serial is None:
            return render_template("glove.html", param=["Install pyserial to use glove mode."])
        t_end = time.time() + 60 * 1
        param = []
        port = os.getenv("GLOVE_PORT", "COM3")
        baud = int(os.getenv("GLOVE_BAUD", "9600"))
        try:
            ser = serial.Serial(port, baud, timeout=2)
        except Exception as exc:
            ports = ", ".join(get_available_ports()) or "none"
            msg = "Could not open {} at {}. {}. Available ports: {}".format(
                port, baud, exc, ports
            )
            return render_template("glove.html", param=[msg])
        predicted_svm="something"
        while True:

            count = 0
            data = []
            while (count < 5):
                # time.sleep(1)
                if (ser.isOpen() == False):
                    ser.open()
                    ser.flushInput()
                    print(count)
                elif (count == 4):
                    data.append(ser.readline())
                    print("if count")
                    ser.close()
                else:
                    data.append(ser.readline())
                    #print(ser.readline())

                    print(count)
                count = count + 1

            data1 = data
            data1.pop(0)
            lines = []
            for line in data1:
                lines.append(line.decode('utf-8', 'slashescape'))
            lines1 = [s.strip('\r\n') for s in lines]
            y = []
            for x in lines1:
                try:
                    vals = [int(v.strip()) for v in x.split(",")]
                except ValueError:
                    continue
                if len(vals) >= 11:
                    y.append(vals)
            print("1")
            if not y:
                predicted_svm = "nothing"
                print("nothing")
                break

            if(int(y[0][10])== 0):
                predicted_svm="nothing"
                print("nothing")
                break

            else:
                for i in range(len(y)):
                    y[i].pop(-1)
                print("1")
                #col_totals = [sum(x) for x in zip(*y)]
                # print(col_totals)
                #means = [int(x / 10) for x in col_totals]
                arr = np.array(y)
                m = stats.mode(arr)
                modes=m[0]
                print(modes)
                predicted_svm = model.predict(modes.reshape(1,-1))
                #predicted_svm = predicted_svm[1:-1]
                speak_text(predicted_svm[0])
                param.append(predicted_svm[0])
                print(param)
                time.sleep(3)
                print("sleep over")
                # return  redirect(url_for('glove'))
        print("something")
        return render_template("glove.html", param=param)
    elif request.method == 'POST':
        return redirect(url_for('index'))
        # return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
