#!/bin/bash
export KMP_DUPLICATE_LIB_OK=TRUE
uvicorn app:app --host 0.0.0.0 --port $PORT
