import json

from geopy.geocoders import Nominatim
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, login_manager
from ecoApi import app, db
from ecoApi.models import User, Reciclaje, MapaDeReciclaje


login_manager = LoginManager(app)
login_manager.init_app(app)

# Le aclaramos a login_manager donde esta ubicada la ruta de inicio de sesion
login_manager.login_view = 'login'
# Configura un user_agent único y descriptivo
geolocator = Nominatim(user_agent="mi_app_geolocalizacion")

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    print(f'ESTE ES EL USUARIO LOGGEADO{user}')
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return "Welcome to the API!"


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Verifica las credenciales en la base de datos
    user = User.query.filter_by(username=username.lower(), password=password).first()

    if user:
        login_user(user)  # Opcional, para iniciar sesión
        print("SESION INICIADA")
        return jsonify({"status": "success", "message": "Valid credentials", "user_id": user.id}), 201
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 400


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    print("SESION CERRADA")
    return jsonify({"status": "success", "message": "Logged out successfully"}), 201


@app.route('/status', methods=['GET'])
def status():
    if current_user.is_authenticated:
        return jsonify({"status": "logged_in", "user": current_user.username}), 200
    else:
        return jsonify({"status": "logged_out"}), 200


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    lastname = data.get('lastname')
    email = data.get('email')
    address = data.get('address')
    password = data.get('password')
    #coordenadas = obtenerCoordenadasDe(f"{address} Argentina") Las respuestas de la api son gratuitas pero lentas
    #coordenada_x = coordenadas['latitud']
    #coordenada_y = coordenadas['longitud']
    # Crear el nuevo usuario
    new_user = User(username=username.lower(), lastname=lastname.lower(), email=email.lower(), address=address,
                    password=password, coordenada_x=None, coordenada_y=None)

    # Añadir el usuario a la base de datos
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"status": "success", "message": "User registered successfully"}), 201


# DIVIDIR EN SUBTAREAS EL RECICLAJE Y EL MAPA
@app.route('/recycling', methods=['POST'])
def recycling():
    data = request.json
    usuario_de_reciclaje = data.get('usuarioId')
    user = User.query.filter_by(id=usuario_de_reciclaje).first()
    if user:
        reciclaje = Reciclaje(
            vidrio=data.get('vidrio', False),
            metal=data.get('metal', False),
            plastico=data.get('plastico', False),
            carton=data.get('carton', False),
            usuario_de_reciclaje=user.id
        )
        db.session.add(reciclaje)
        db.session.commit()

        mapa_reciclaje = MapaDeReciclaje(
            reciclaje_id=reciclaje.id,
            direccion=user.address,
            coordenada_x=None,  # ACA TENEMOS QUE CONSULTAR POR LAS COORDENADAS, SI NO SE ENCUENTRA DEVUELVE NONE
            coordenada_y=None,
            recolector_id=None  # Asignar recolector_id si es necesario
        )
        db.session.add(mapa_reciclaje)
        db.session.commit()

        # Emitir los datos actualizados a todos los clientes

        return jsonify({"status": "success", "message": "Reciclaje añadido y mapa actualizado"}), 201
    else:
        return jsonify({"status": "error", "message": "User not found"}), 400


@app.route('/open_map', methods=['GET'])
def open_map():
    # Consulta todos los registros de la tabla mapa_de_reciclaje
    mapa_data = MapaDeReciclaje.query.filter_by(estado='disponible').all()

    # Crear una lista de diccionarios con los datos del mapa
    map_data_list = [{
        'reciclaje_id': item.reciclaje_id,
        'direccion': item.direccion,
        'coordenada_x': item.coordenada_x,
        'coordenada_y': item.coordenada_y,
        'recolector_id': item.recolector_id
    } for item in mapa_data]

    return jsonify({"status": "success", "map_data": map_data_list}), 201


def obtenerCoordenadasDe(direccion_a_buscar):
    try:
        # Obtener la ubicación
        direccion = f'{direccion_a_buscar}, Argentina'
        ubicacion = geolocator.geocode(direccion)

        # Verificar si la ubicación es válida y no es None
        if ubicacion:
            # Retornar un diccionario con latitud y longitud
            return {
                'latitud': ubicacion.latitude,
                'longitud': ubicacion.longitude
            }
        else:
            print("Ubicación no encontrada.")
            return {'latitud': None, 'longitud': None}  # o podrías retornar valores predeterminados como 0 o -1
    except Exception as e:
        print(f"Error al obtener la ubicación: {e}")
        return {'latitud': None, 'longitud': None}
