FROM ubuntu:22.04

RUN apt update && apt install -y python3 && apt install -y pip
WORKDIR /chatgpt
COPY ./app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app/ .
ENV API_KEY="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"

ENV client_secret=agU8Q~1Ae~8NuqgXILZEBlyqmZ6tNoUx0cKPRaj3 
ENV client_id=4efd5306-6b56-440b-9bbd-5b3d9414fa03
ENV tenant_id=28d1eaf4-0022-4840-8257-173c1bd0de0f 
ENV redirect_url="https://chatgpt.germanywestcentral.cloudapp.azure.com/getToken"
ENV SNOWFLAKE_ACCOUNT="zv53059.eu-central-1"
ENV SNOWFLAKE_USER="yosuke.yoshida@adragos-pharma.com"
ENV SNOWFLAKE_PASSWORD="Jp026939!"
ENV SNOWFLAKE_DATABASE="YOSUKEYOSHIDA_PREP"
ENV SNOWFLAKE_WAREHOUSE="WH_XS_KAW"
ENV SNOWFLAKE_SCHEMA="CHATGPT"
ENV SNOWFLAKE_ROLE="YOSUKEYOSHIDA"
#COPY ./dev_certs ./
#CMD ["python3", "app.py"]
CMD [ "gunicorn", "app:app", "-c","gunicorn_config.py"]
#CMD [ "gunicorn", "app:app", "-c","gunicorn_config.py", "--keyfile", "./private-key.pem", "--certfile", "./public-key.pem"]