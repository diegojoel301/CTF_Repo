from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        data = request.form  # Obtiene todos los datos enviados en el formulario
        print(data)
        return f'Los datos enviados son: {data}'
    else:
        return 'Hola, por favor envía datos a través de POST.'

if __name__ == '__main__':
    app.run(debug=True)
