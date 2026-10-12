import sys
import os
import uvicorn

# Add project root directory to Python module search path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    from backend.app.main import app
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
