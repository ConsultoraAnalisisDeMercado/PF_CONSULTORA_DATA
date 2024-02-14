from google.cloud import bigquery
import pandas as pd
import functions_framework

@functions_framework.http
def top_hoteles_por_ubicacion(request):
    # Extrae los parámetros de la solicitud y realiza la corrección
    estado = request.args.get('estado', '').upper()
    ciudad = request.args.get('ciudad', '').title()

    # Validación de parámetros
    if not estado or not ciudad:
        return {"error": "Se requieren tanto 'estado' como 'ciudad' en la solicitud."}, 400

    try:
        # Configura el cliente de BigQuery
        bigquery_client = bigquery.Client()

        # Construye la consulta SQL
        query = f"""
            SELECT name, stars, review_count
            FROM ``
            WHERE state = '{estado}' AND city = '{ciudad}'
            ORDER BY stars DESC, review_count DESC
            LIMIT 5
        """

        # Ejecuta la consulta y obtén los resultados
        query_job = bigquery_client.query(query)
        results = query_job.result()

        # Convierte los resultados a un DataFrame de pandas
        hoteles = pd.DataFrame(data=[(row['name'], row['stars'], row['review_count']) for row in results],
                               columns=['name', 'stars', 'review_count'])

        if hoteles.empty:
            return {"mensaje": "No se encontraron hoteles en la ubicación proporcionada."}
        else:
            # Toma los primeros 5 hoteles
            top_hoteles = hoteles.head(5)

            return {"mensaje": "El top de hoteles para tu ubicación es", "hoteles": top_hoteles.to_dict(orient='records')}

    except Exception as e:
        return {"error": f"Error al procesar la solicitud: {str(e)}"}, 500