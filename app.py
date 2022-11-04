from flask import Flask, render_template
from flask_mysqldb import MySQL
from os import environ
#sirve para leer el archivo .env y carga las variables definidas en ese archivo como variables de entorno
from dotenv import load_dotenv

load_dotenv()

app = Flask (__name__)
#app.config['USUARIO'] = 'eduardo' añade variable eduardo a diccionario  'config'
#TODAS LAS VARIABLES DE ENTORNO SERAN STRING
app.config['MYSQL_HOST'] = environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = environ.get('MYSQL_DB')
app.config['MYSQL_PORT'] = int(environ.get('MYSQL_PORT'))

# --print(app.config) --almacena todas las variables de configuracion de FLASK

mysql = MySQL(app)

# Un decorador es la forma en la cual modificamos el comportamiento de una clase sin la necesidad de modificarlo directamente, es como usar la herencia para modificar su comportamiento, dependiendo de su ruta y su metodo
@app.route('/',methods=['GET'])
def inicio():
    return{
        'message': 'Bienvenido a mi API de colegios'
    }

@app.route('/inicio',methods=['GET'])
def pagina_inicial():
    return render_template('inicio.html')

@app.route('/mostrar-alumnos', methods=['GET'])   
def devolver_alumnos():
    #crea  una conexion en la base de datos
    cursor = mysql.connection.cursor()
    #ejecutamos una clausura hacia una determinada tabla
    cursor.execute("SELECT * FROM alumnos")
    #devolver toda la informacion de esa consulta
    resultado = cursor.fetchall()
    print(resultado)
    resultado_final = []
    for alumno in resultado:
        print(alumno)
        alumno_diccionario ={
            'id':alumno[0],
            'nombre':alumno[1],
            'ape_paterno':alumno[2],
            'ape_materno':alumno[3],
            'correo':alumno[4],
            'num_emergencia':alumno[5],
            'curso_id':alumno[6]
        }
        print(alumno_diccionario)
        resultado_final.append(alumno_diccionario)
    #return {
    #    'message':'los alumnos son:',
    #    'content': resultado_final
    #}
    return render_template('mostrar_alumnos.html',alumnos=resultado_final, mensaje='hola desde Flask')

@app.route("/agregar-alumnos",methods =['GET'])   
def agregar_alumno():
    return render_template('agregar_alumno.html')


app.run(debug=True)

