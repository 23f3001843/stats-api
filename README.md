# Stats API — Deployment Guide

## Before deploying, open `main.py` and change:
1. `YOUR_EMAIL` → your actual login email
2. `ALLOWED_ORIGIN` → already set to `https://dash-aji2l6.example.com`

## Deploy to Railway (you're already there!)
1. Push these files to your GitHub repo
2. Railway auto-detects and redeploys
3. Done!

## Test locally first:
```bash
pip install fastapi uvicorn
uvicorn main:app --reload
# Then visit: http://localhost:8000/stats?values=1,2,3,4,5
```
