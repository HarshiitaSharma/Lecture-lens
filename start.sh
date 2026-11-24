#!/bin/bash
# One container, two processes: FastAPI on 8000 (internal) and Streamlit on 7860 (public).
uvicorn backend.main:app --host 127.0.0.1 --port 8000 &
exec streamlit run frontend/app.py \
  --server.port 7860 --server.address 0.0.0.0 --server.headless true \
  --server.enableXsrfProtection false --server.enableCORS false
