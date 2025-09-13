# SILA Backend

Backend service for SILA System built with FastAPI.

## Setup

1. Create a virtual environment:
   `ash
   python -m venv venv
   .\venv\Scripts\activate
   `

2. Install dependencies:
   `ash
   pip install -r requirements.txt
   `

3. Set up environment variables in .env file

4. Run migrations:
   `ash
   alembic upgrade head
   `

5. Start the server:
   `ash
   uvicorn app.main:app --reload
   `
"@

    # Frontend
    "frontend/package.json" = @"
{
  "name": "sila-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^5.14.1",
    "@testing-library/react": "^12.0.0",
    "@testing-library/user-event": "^13.2.1",
    "axios": "^0.25.0",
    "react": "^17.0.2",
    "react-dom": "^17.0.2",
    "react-router-dom": "^6.2.1",
    "react-scripts": "4.0.3",
    "web-vitals": "^2.1.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
