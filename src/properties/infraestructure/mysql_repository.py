from mysql.connector import Error
from src.properties.domain.repositories import PropertyRepository
from src.properties.domain.schemas import PropertyResponse, PropertyRequest
from src.properties.infraestructure.mysql_conn import DatabaseConnection
import os


class MySQLPropertyRepository(PropertyRepository):

    def __init__(self):
        self.db = DatabaseConnection()

    
    def get_all(self) -> list[PropertyResponse]:
        try:
            connection = self.db.get_connection()
            base_query = os.getenv("MYSQL_QUERY_BASE_PROPERTY")
            base_query += " WHERE s.name IN ('pre_venta', 'en_venta', 'vendido')"
            cursor = connection.cursor(dictionary=True)

            cursor.execute(base_query)
            results = cursor.fetchall()

            return results

        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                self.db.close_connection(connection)


    def get_all_filters(self, property:PropertyRequest= None)-> list[PropertyResponse]:
       pass
