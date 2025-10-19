from pymongo.errors import PyMongoError, ConnectionFailure


class LoginController:
    def __init__(self, mongo):
        self.collection = mongo.db["users"]

    # FALTA: Control de errores de base de datos
    # - Manejar errores de conexión a MongoDB
    # - Validar parámetros de entrada (email no vacío)
    # - Logs para debugging cuando hay problemas
    def get_user(self, email):
        try:
            if not email or not email.strip():
                raise ValueError("Email no puede estar vacío")

            user = self.collection.find_one({"email": email.strip()})
            return user
        except ConnectionFailure:
            print("Error: Fallo en la conexión a la base de datos")
            raise
        except PyMongoError as e:
            print(f"Error de MongoDB en get_user: {e}")
            raise
        except Exception as e:
            print(f"Error inesperado en get_user: {e}")
            raise

    # FALTA: Validación de datos y control de errores
    # - Verificar que user_data contenga campos requeridos
    # - Manejar errores de inserción (duplicados, etc.)
    def create_user(self, user_data):
        try:
            if not user_data:
                raise ValueError("user_data no puede estar vacío")

            # Validar campos requeridos
            required_fields = ["email", "password", "name"]
            for field in required_fields:
                if field not in user_data or not str(user_data[field]).strip():
                    raise ValueError(f"Campo requerido '{field}' faltante o vacío")

            self.collection.insert_one(user_data)
        except ConnectionFailure:
            print("Error: Fallo en la conexión a la base de datos")
            raise
        except PyMongoError as e:
            print(f"Error de MongoDB en create_user: {e}")
            raise
        except Exception as e:
            print(f"Error inesperado en create_user: {e}")
            raise

    # FALTA: Validación y confirmación de eliminación
    # - Verificar que el usuario existe antes de eliminarlo
    # - Retornar información sobre si se eliminó algo
    def delete_user(self, email):
        try:
            if not email or not email.strip():
                raise ValueError("Email no puede estar vacío")

            result = self.collection.delete_one({"email": email.strip()})
            if result.deleted_count == 0:
                raise ValueError(f"Usuario con email '{email}' no encontrado")
            return result.deleted_count
        except ConnectionFailure:
            print("Error: Fallo en la conexión a la base de datos")
            raise
        except PyMongoError as e:
            print(f"Error de MongoDB en delete_user: {e}")
            raise
        except Exception as e:
            print(f"Error inesperado en delete_user: {e}")
            raise

    # FALTA: Control de errores en consultas masivas
    # - Limitar número de resultados para evitar sobrecarga
    # - Manejar errores de memoria si hay muchos usuarios
    def get_all_users(self):
        try:
            # Limitar a 1000 usuarios para evitar problemas de memoria
            users_cursor = self.collection.find({}, {"_id": 0}).limit(1000)
            return list(users_cursor)
        except ConnectionFailure:
            print("Error: Fallo en la conexión a la base de datos")
            raise
        except PyMongoError as e:
            print(f"Error de MongoDB en get_all_users: {e}")
            raise
        except Exception as e:
            print(f"Error inesperado en get_all_users: {e}")
            raise
