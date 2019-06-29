from flask import Flask
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)

class Inference(Resource):
    def get(self):
        output = {}
        with open('output.txt', 'r') as f:
            for line in f:
                list_line = line.split(',')
                output[list_line[0]] = list_line[1][:-1]

        return output

api.add_resource(Inference, '/inference')

if __name__=="__main__":
    app.run(debug=True)