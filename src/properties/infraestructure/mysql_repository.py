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
        connection = None
        cursor = None
        try:
            connection = self.db.get_connection()
            base_query = os.getenv("MYSQL_QUERY_BASE_PROPERTY")
            if not base_query:
                raise ValueError("MYSQL_QUERY_BASE_PROPERTY environment variable not found")
            
            base_query += " WHERE s.name IN ('pre_venta', 'en_venta', 'vendido')"
            cursor = connection.cursor(dictionary=True)

            cursor.execute(base_query)
            results = cursor.fetchall()

            list_response = self._parse_data(results)

            return list_response

        except Error as e:
            logger.error(f"Error al ejecutar la consulta: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                self.db.close_connection(connection)

    def get_all_filters(self, property: PropertyRequest = None) -> list[PropertyResponse]:
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
        connection = None
        cursor = None
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor(dictionary=True)

            query, params = self._extract_filters(property=property)
            
            cursor.execute(query, tuple(params))
            results = cursor.fetchall()

            list_response = self._parse_data(results)

            return list_response

        except Error as e:
            logger.error(f"Error al ejecutar la consulta con parametros: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                self.db.close_connection(connection)


    def _extract_filters(self, property: PropertyRequest) -> tuple[str, list]:
        """
        Constructs a SQL query string with dynamic filters based on the provided PropertyRequest object.
        This method appends SQL conditions to a base query depending on the presence of 'estado', 'ciudad', and 'anio'
        attributes in the PropertyRequest. If 'estado' is not provided, it defaults to filtering by a set of predefined states.
        Args:
            property (PropertyRequest): The property request object containing filter criteria.
        Returns:
            Tuple[str, List]: A tuple containing the constructed SQL query string and a list of parameters for the query.
        Raises:
            Exception: If any error occurs during the construction of the query or parameter list.
        """
        try:
            query_base = os.getenv("MYSQL_QUERY_BASE_PROPERTY")
            if not query_base:
                raise ValueError("MYSQL_QUERY_BASE_PROPERTY environment variable not found")
            
            params = []
            where_conditions = []

            # Handle estado filter
            if property.estado:
                where_conditions.append("s.name = %s")
                params.append(property.estado)
            else:
                where_conditions.append("s.name IN ('pre_venta', 'en_venta', 'vendido')")
            
            # Handle ciudad filter
            if property.ciudad:
                where_conditions.append("p.city = %s")
                params.append(property.ciudad)
            
            # Handle año filter
            if property.anio:
                where_conditions.append("p.year = %s")
                params.append(property.anio)
            
            # Combine all conditions
            if where_conditions:
                query_base += " WHERE " + " AND ".join(where_conditions)
            
            return query_base, params
            
        except Exception as e:
            logger.error(f"Error en _extract_filters: {e}")
            raise e

    def _parse_data(self, raw_data: list) -> list[PropertyResponse]:
        """
        Parses a list of raw data dictionaries into a list of PropertyResponse objects.
        Args:
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
                except ValueError as e:
                    logger.warning(f"Skipping invalid property data: {e}")
                    continue
            
            return list_response_obj

        except Exception as e:
            logger.error(f"Error en _parse_data: {e}")
            raise e
    
