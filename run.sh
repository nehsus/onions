#!/bin/bash
echo "Initializing backend.."
cd backend && 
    python3 -m venv opinion_env &&
    source opinion_env/bin/activate &&
    pip3 install -r requirements.txt &&
    echo "done!" &&
    
echo "init ui.." &&
cd ../ &&
    npm install --save &&
    echo "done!" &&
    npm run start