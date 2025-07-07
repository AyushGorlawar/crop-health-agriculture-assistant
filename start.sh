#!/bin/bash

echo "Starting Crop Health & Agriculture Assistant..."
echo

echo "Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting Flask backend..."
python app.py &
BACKEND_PID=$!

cd ..

echo
echo "Setting up frontend..."
cd frontend

echo "Starting frontend server..."
python3 -m http.server 8000 &
FRONTEND_PID=$!

cd ..

echo
echo "Application is starting..."
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:8000"
echo
echo "Press Ctrl+C to stop both servers..."

# Wait for user to stop
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait 