# Blog Site

It's a simple Web API built with Python framework FastAPI that allows users to add new user, new blog and retrieve all blogs of a particular user with pagination support.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RehberOdhano/Blog-Site.git
   cd Blog-Site
   ```
2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install required packages/libraries:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Setup the database:**
   Modify the ```SQLALCHEMY_DATABASE_URL``` in ```config.py``` file to point to your local database.
5. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```
    
   
