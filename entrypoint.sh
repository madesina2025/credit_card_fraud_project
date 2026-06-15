#!/bin/bash

# Start JupyterLab in the background
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser \
  --NotebookApp.token='' \
  --NotebookApp.allow_origin='*' \
  --NotebookApp.allow_remote_access=True \
  --allow-root &


echo "Starting dashboard script..."

# Start Dash dashboard
#python dashboard/dash_app.py

# Run Dash app
python3 /app/dashboard/dash_app.py &

# Keep container alive (waits for background process)
wait
