# [START functions]
import functions_framework
import os
import requests
import pandas as pd
import logging


# Realizar la solicitud HTTP
def request_yelp(api_key, params):
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()

def request_reviews(api_key, business_id):
    url = f"https://api.yelp.com/v3/businesses/{business_id}/reviews"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Normalizar la respuesta JSON y convertirla en un data frame
def normalize(json_response):
    table_id="businesses"
    # seleccionar la columna "businesses"
    businesses = json_response[table_id]    
    # Convertir el objeto JSON en un DataFrame de pandas
    df = pd.json_normalize(businesses)
    # Renombrar las columnas
    df = df.rename(columns={"id": "business_id"})
    df = df.rename(columns={"rating": "business_stars"})
    df = df.rename(columns={"coordinates.latitude": "latitude"})
    df = df.rename(columns={"coordinates.longitude": "longitude"})
    df = df.rename(columns={"location.address1": "address1"})
    df = df.rename(columns={"location.address2": "address2"})
    df = df.rename(columns={"location.address3": "address3"})
    df = df.rename(columns={"location.city": "city"})
    df = df.rename(columns={"location.zip_code": "postal_code"})
    df = df.rename(columns={"location.country": "country"})
    df = df.rename(columns={"location.state": "state"})
    df = df.rename(columns={"location.display_address": "address"})    

    # Convertir la columna postal_code a tipo float
    df["postal_code"] = df["postal_code"].astype(float)

    # Extraer valor de title de categories y guardar un string separado por comas
    df["categories"] = df["categories"].apply(lambda x: ", ".join([y["title"] for y in x]))
    # Convertir address en string separado por espacios
    df["address"] = df["address"].apply(lambda x: " ".join(x))
 
    # Seleccionar las columnas que se van a usar
    fields = ["business_id", "name", "address","postal_code", "city", "state", "latitude", "longitude", "categories","business_stars"]
    df = df[fields]
    print(df.dtypes)
    return df

def normalize_review(json_response,business_id):
    table_id="reviews"
    # seleccionar la columna "reviews"
    reviews = json_response[table_id]    
    # Convertir el objeto JSON en un DataFrame de pandas
    df = pd.json_normalize(reviews)
    # Renombrar las columnas
    df = df.rename(columns={"id": "review_id"})
    df = df.rename(columns={"rating": "review_stars"})
    df = df.rename(columns={"time_created": "date"})
     # Agregar la columna business_id
    df["business_id"] = business_id

    # Convertir la columna "date" a tipo de dato timestamp
    df["date"] = pd.to_datetime(df["date"])

    # Seleccionar las columnas que se van a usar
    fields = ["business_id","review_id", "review_stars", "date"]
    df = df[fields]
    print(df["date"])
    print(df.dtypes)
    return df

# Guardar un data frame en GCS
def df_to_bq(df, destination_table, project_id):
    """
    Guarda un dataframe de pandas en BigQuery
    """
    # guardar en BigQuery
    try:
        df.to_gbq(destination_table=destination_table, project_id=project_id, if_exists="append")
    except Exception as e:
        logging.error(f"Error al escribir en BigQuery: {e}")
        raise


def req_normalize_marge(df, api_key1, api_key2):
    df_reviews_final = pd.DataFrame()

    # Obtener los dos primeros business_id
    ids = df["business_id"].tolist()
    
    for business_id in ids:
        # Alternar entre las dos API keys
        current_api_key = api_key1 if ids.index(business_id) % 2 == 0 else api_key2

        # Realizar la solicitud de revisión
        reviews_data = request_reviews(current_api_key, business_id)

        # Normalizar la respuesta de revisión y almacenarla en un DataFrame temporal
        df_reviews_temp = normalize_review(reviews_data,business_id)

        # Concatenar los resultados al DataFrame final
        df_reviews_final = pd.concat([df_reviews_final, df_reviews_temp], ignore_index=True)

    # Combinar el DataFrame de revisiones con el DataFrame original en función de business_id
    combined_df_business_reviews = pd.merge(df_reviews_final, df, on='business_id', how='inner')
    return combined_df_business_reviews




# Función de entrada
@functions_framework.http
def api_yelp_consulta(request):
    try:
        # Extrae los parámetros de la solicitud y realiza la corrección
        estado = request.args.get('estado', '').upper()

        # Verificar si el estado está permitido
        allowed_states = ['CA', 'OR', 'WA', 'AZ', 'NV']
        if estado not in allowed_states:
            logging.error(f"Estado no permitido: {estado}")
            return "Estado no permitido", 400

        ciudad = request.args.get('ciudad', '').title()

        # CONSTANTES
        GCP_PROJECT = os.environ.get("GCP_PROJECT")    
        YELP_CLIENT_ID= ""
        YELP_API_KEY= ""
        YELP_API_KEY2=""
        GCP_PROJECT= ""
        GCP_REGION=  ""

        # Selecciono la categoría en Yelp que seo buscar y analizar
        category = "hotels"
        # Cargar la respuesta JSON en un objeto Python
        params = f"categories={category}&location={ciudad}, {estado}"
        # Realizar la solicitud HTTP
        data = request_yelp(YELP_API_KEY, params)
        # Normalizar la respuesta JSON y convertirla en un dataframe
        df = normalize(data)

        df_final = req_normalize_marge(df,YELP_API_KEY,YELP_API_KEY2)

        # tabla de destino
        destination_table = ""
        # Obtener la cantidad de registros nuevos
        num_records = df_final.shape[0]
        df_to_bq(df_final, destination_table, GCP_PROJECT)

        # Construir el mensaje de retorno
        return f"OK. {num_records} registros nuevos cargados exitosamente en BigQuery"
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        return "Error inesperado", 500

# [END functions]