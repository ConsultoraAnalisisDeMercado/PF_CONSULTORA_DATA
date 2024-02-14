# Importar las bibliotecas necesarias
import logging
from google.cloud import bigquery
import functions_framework

@functions_framework.http
def update_table(request):
    try:
        # CONSTANTES
        project_id = ""
        dataset_id_source = ""
        table_id_source = ""
        dataset_id_destination = ""
        table_id_destination = ""

        client = bigquery.Client(project=project_id)

        # Obtener datos de la tabla de origen
        query_source = f"SELECT * FROM `{project_id}.{dataset_id_source}.{table_id_source}`"
        query_job_source = client.query(query_source)
        results = query_job_source.result()

        # Convertir resultados a DataFrame
        df = results.to_dataframe()

        # Validar review_id antes de insertar
        existing_review_ids_query = f"SELECT review_id FROM `{project_id}.{dataset_id_destination}.{table_id_destination}`"
        existing_review_ids = set(client.query(existing_review_ids_query).to_dataframe()["review_id"])

        # Filtrar DataFrame para obtener solo las filas que no están en la tabla de destino
        df_to_insert = df[~df["review_id"].isin(existing_review_ids)]

        # Ingestar datos en la tabla de destino
        if not df_to_insert.empty:
            job_config = bigquery.LoadJobConfig()
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
            job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED

            destination_table_ref = client.dataset(dataset_id_destination).table(table_id_destination)
            job = client.load_table_from_dataframe(df_to_insert, destination_table_ref, job_config=job_config)
            job.result()

        # Eliminar los registros de la tabla de origen
        if not df.empty:
            delete_query = f"DELETE FROM `{project_id}.{dataset_id_source}.{table_id_source}` WHERE review_id IN UNNEST({list(df['review_id'])})"
            delete_job = client.query(delete_query)
            delete_job.result()

        num_rows_inserted = len(df_to_insert)
        num_rows_repeated = len(df) - num_rows_inserted

        return f"Se realizaron correctamente {num_rows_inserted} registros. {num_rows_repeated} registros ya existían y no se ingresaron. Registros eliminados de la tabla de origen: {len(df)}"
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        return "Error"