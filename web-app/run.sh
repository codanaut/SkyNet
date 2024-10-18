#uvicorn test-app:app --reload --host 0.0.0.0 --port 2222 --proxy-headers --forwarded-allow-ips "*" 

#gunicorn test-app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:2222

gunicorn skynet-app:app -w 4 -k uvicorn_worker.UvicornWorker --bind 0.0.0.0:2222