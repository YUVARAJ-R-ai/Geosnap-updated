#!/data/data/com.termux/files/usr/bin/bash
source ~/fastapi/venv/bin/activate
export PYTHONPATH=$HOME/fastapi
uvicorn app.main:app --reload &
