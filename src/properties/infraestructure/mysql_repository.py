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

            list_reponse = self._parse_data(results)

            return list_reponse

        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                self.db.close_connection(connection)


    def get_all_filters(self, property:PropertyRequest= None)-> list[PropertyResponse]:
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor(dictionary=True)

            query, params = self._extract_filters(property=property)
            
            cursor.execute(query, tuple(params))
            results = cursor.fetchall()

            return results

        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                self.db.close_connection(connection)


    def _extract_filters(self, property: PropertyRequest) -> str:
        try:
            query_base = os.getenv("MYSQL_QUERY_BASE_PROPERTY")
            
            params = []

            if property.estado:
                query_base += " AND s.name = %s"
                params.append(property.estado)
            else:
                where_param = " WHERE s.name IN ('pre_venta', 'en_venta', 'vendido')"
                query_base += where_param
            
            if property.ciudad:
                query_base += " AND p.city = %s"
                params.append(property.ciudad)
            
            if property.anio_construcion:
                query_base += " AND p.year = %s"
                params.append(property.anio_construcion)
            
            return query_base, params
        
        except Exception as e:
            raise RuntimeError(e)


    def _parse_data(sell, raw_data:list) -> list[PropertyResponse]:
        try:

            list_response_obj = []
            for data in raw_data:
                try:
                    new_object = PropertyResponse(**data)
                    list_response_obj.append(new_object)
                except ValueError:
                    pass
            
            return list_response_obj

        except Exception as e:
            raise e
    
