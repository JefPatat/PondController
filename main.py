import relaycontroller
from PumpDescription import PumpDescription
from config import config
from TimesForm import TimesForm

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

relaycontroller.scheduled_task()

scheduler = BackgroundScheduler()
scheduler.add_job(func=relaycontroller.scheduled_task, trigger="interval", seconds=60)
scheduler.start()

pumpDescriptions = []

for pump in config["pumps"]:
   pumpDescriptions.append(PumpDescription(pump["name"], False, pump["pin"], pump["pumpOnIntervals"]))

def updatePumpStates():
   for pumpDescription in pumpDescriptions:
      pumpDescription.State = relaycontroller.GetPumpState(pumpDescription.Pin)

@app.route("/")
def main():
   updatePumpStates()
   return render_template('main.html', pumpDescriptions=pumpDescriptions)

@app.route('/times')
def times():
   form = TimesForm()
   return render_template('times.html', form = form)

@app.route("/<pumpPin>/<action>")
def action(pumpPin, action):
   pumpPin = int(pumpPin)

   if action == "on":
      relaycontroller.SetPump(pumpPin, True)
      updatePumpStates()
      return render_template('main.html', pumpDescriptions = pumpDescriptions)

   if action == "off":
      relaycontroller.SetPump(pumpPin, False)
      updatePumpStates()
      return render_template('main.html', pumpDescriptions = pumpDescriptions)

   if action == "setOnIntervals":
      for pumpDescription in pumpDescriptions:
         if pumpDescription.Pin == pumpPin:
            form = TimesForm()
            return render_template('times.html', form = form, pumpDescription = pumpDescription)
   

@app.route('/success',methods = ['GET','POST'])  
def success():  
   return render_template("success.html") 

@app.route("/settimes", methods=["GET", "POST"])
def settimes():
   if request.method == "POST":
      flash('Login successful', 'success')
      return redirect("/success")
   return render_template("settimes.html")

   
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='192.168.1.107')