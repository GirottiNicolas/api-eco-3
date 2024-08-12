from flask_login import LoginManager, UserMixin
from ecoApi import app, db, login_manager


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    print(f'ESTE ES EL USUARIO LOGGEADO{user}')
    return User.query.get(int(user_id))


# Al crear una nueva tabla: flask db migrate -m "descripcion" y luego flask db upgrade

# Defini tablas en base de datos mysql
class User(db.Model, UserMixin):
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    lastname = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    tieneReciclaje = db.Column(db.Boolean, default=False) # ELIMINAR
    coordenada_x = db.Column(db.Float, nullable=True)
    coordenada_y = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Reciclaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vidrio = db.Column(db.Boolean, default=False)
    metal = db.Column(db.Boolean, default=False)
    plastico = db.Column(db.Boolean, default=False)
    carton = db.Column(db.Boolean, default=False)
    usuario_de_reciclaje = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    usuario_recolector_en_camino = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=True) # ELIMINAR


class MapaDeReciclaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reciclaje_id = db.Column(db.Integer, db.ForeignKey('reciclaje.id'), nullable=False)
    direccion = db.Column(db.String(255), nullable=False) # ELIMINAR
    estado = db.Column(db.Enum('disponible', 'en camino', 'recogido'), default='disponible')
    coordenada_x = db.Column(db.Float, nullable=True)  # ELIMINAR
    coordenada_y = db.Column(db.Float, nullable=True)  # ELIMINAR
    recolector_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=True) # ELIMINAR


db.init_app(app)
with app.app_context():
    db.create_all()