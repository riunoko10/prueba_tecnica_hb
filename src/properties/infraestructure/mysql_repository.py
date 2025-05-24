from mysql.connector import Error
from src.properties.domain.repositories import PropertyRepository
from src.properties.domain.schemas import PropertyResponse, PropertyRequest
from src.properties.infraestructure.mysql_conn import DatabaseConnection
import os

from src.shared.infraestructure.logger import get_logger

logger = get_logger(__name__)

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
            logger.error(f"Error al ejecutar la consulta: {e}")
            raise(e)
        finally:
            if connection.is_connected():
                cursor.close()
                self.db.close_connection(connection)

    def get_all_filters(self, property:PropertyRequest= None)-> list[PropertyResponse]:
        """
        Retrieves a list of properties from the database based on the provided filters.
        Args:
            property (PropertyRequest, optional): An object containing filter criteria for querying properties.
                If None, all properties are retrieved.
        Returns:
            list[PropertyResponse]: A list of PropertyResponse objects matching the filter criteria.
        Raises:
            Error: If an error occurs during the database query execution.
        Logs:
            Logs an error message if the query execution fails.
        """
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor(dictionary=True)

            query, params = self._extract_filters(property=property)
            
            cursor.execute(query, tuple(params))
            results = cursor.fetchall()

            list_reponse = self._parse_data(results)

            return list_reponse

        except Error as e:
            logger.error(f"Error al ejecutar la consulta con parametros: {e}")
            raise(e)
        finally:
            if connection.is_connected():
                cursor.close()
                self.db.close_connection(connection)


    def _extract_filters(self, property: PropertyRequest) -> str:
        """
        Constructs a SQL query string with dynamic filters based on the provided PropertyRequest object.
        This method appends SQL conditions to a base query depending on the presence of 'estado', 'ciudad', and 'anio'
        attributes in the PropertyRequest. If 'estado' is not provided, it defaults to filtering by a set of predefined states.
        Args:
            property (PropertyRequest): The property request object containing filter criteria.
        Returns:
            Tuple[str, List[Any]]: A tuple containing the constructed SQL query string and a list of parameters for the query.
        Raises:
            Exception: If any error occurs during the construction of the query or parameter list.
        """
        try:
            query_base = os.getenv("MYSQL_QUERY_BASE_PROPERTY")
            params = []

            logger.info(params)

            if property.estado:
                query_base += " AND s.name = %s"
                params.append(property.estado)
            else:
                where_param = " WHERE s.name IN ('pre_venta', 'en_venta', 'vendido')"
                query_base += where_param
            
            if property.ciudad:
                query_base += " AND p.city = %s"
                params.append(property.ciudad)
            
            if property.anio:
                query_base += " AND p.year = %s"
                params.append(property.anio)
            
            return query_base, params
        except Exception as e:
            logger.error(f"Error en _extract_filters: {e}")
            raise(e)

    def _parse_data(sell, raw_data:list) -> list[PropertyResponse]:
        """
        Parses a list of raw data dictionaries into a list of PropertyResponse objects.
        Args:
            sell: Unused parameter, kept for compatibility.
            raw_data (list): A list of dictionaries containing property data.
        Returns:
            list[PropertyResponse]: A list of PropertyResponse objects created from the raw data.
        Raises:
            Exception: If an unexpected error occurs during parsing.
        Notes:
            - Any dictionary in raw_data that cannot be converted to a PropertyResponse due to a ValueError is skipped.
            - Errors are logged using the logger.
        """
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
            logger.error(f"Error en _parse_data: {e}")
            raise (e)
    
