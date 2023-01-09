#!/bin/bash
redis-server --daemonize yes
uvicorn stf.entrypoints.app:app --host 0.0.0.0 --port 3500
