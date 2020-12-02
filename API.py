import os
import config
from flask import Flask, request, send_file
from flask_restful import Resource, Api
from flask_cors import CORS
from twilio.rest import Client
import db_connector as db
import time

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


class MESSAGE(Resource):

  def post(self):
        
    number = request.form['From']
    message_body = request.form['Body'].lower() # message enviado
    message = "No estas registrado en la base de datos."

                
    client = Client(config.ACCOUNT_SID, config.AUTH_TOKEN)

    exist, username = db.findUser(number) 

    if not exist:
        # El Paciente no esta registrado
        message = client.messages.create(
                            from_='whatsapp:+14155238886',  
                            body=message,
                            to=number)
    else:

        if message_body == "hola":
            message = f"Hola, {username}!"        
            message = client.messages.create (
                                    from_='whatsapp:+14155238886',  
                                    body=message,
                                    to=number
                                    )

        print(message_body.find("consulta"))
        
        # El paciente si esta registrado                        
        if message_body.find("consulta") != -1:
            print("Se requiere una consulta.")
            # Si se requiere una consulta del pulso cardiaco
            if (message_body.find("heart rate") != -1) or (message_body.find("pulso cardiaco") != -1) or (message_body.find("pulso") != -1): 
                message = f"{username} esta es la información actual de tus registros de pulso cardiaco."        
                message = client.messages.create (
                                        from_='whatsapp:+14155238886',  
                                        body=message,
                                        # media_url=['https://e1d59601d333.ngrok.io/image?number='+number],
                                        to=number
                                    )
            # Si se requiere una consulta de concentracion de oxigeno
            if (message_body.find("concentracion oxigeno") != -1) or (message_body.find("oxigeno") != -1) or (message_body.find("spo2") != -1):
                message = f"{username} esta es la información actual de tus registros de concentracion de oxigeno."        
                message = client.messages.create (
                                        from_='whatsapp:+14155238886',  
                                        body=message,
                                        # media_url=['https://e1d59601d333.ngrok.io/image?number='+number],
                                        to=number
                                    )     

class IMAGE(Resource):
    def get(self):        
        number = request.args.get('number')
        number = number.replace(": ","_+")        
        print(number)
        db.create_img(number)
        filename = number+'.png'
        return send_file(filename, mimetype='image/png')

api.add_resource(MESSAGE, '/message')  # Route_1
# api.add_resource(IMAGE, '/image')  # Route_2

if __name__ == '__main__':
    app.run(port='5013')