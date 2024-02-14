REGION=us-west1
YOUR_FUNCTION_NAME=update_table
ENTRY_POINT=main

gcloud functions deploy $YOUR_FUNCTION_NAME \
    --gen2 \
    --runtime=python310 \
    --region=$REGION \
    --trigger-http \
    --entry-point=$ENTRY_POINT \
    --env-vars-file .env.yaml \
    --memory 512MB \
    --source=.