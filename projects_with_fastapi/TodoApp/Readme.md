Here is a TodoApp application with fastapi and sqllite. Will port database to postgres soon and also will add docker file and test files. 


To Run:

1. create venv and run requirements.txt to install dependencies. 
2. Create an sqlite db file in the TodoApp directory. 
3. Generate a secret key for encryption by running `openssl rand -hex 32` in your terminal. 
4. Export the following into your system environment (Will add bash script to do that soon)
    * `export SECRET_KEY= "<your secret key generate in step 2>"`
    * `export ALGORITHM="HS256"`
    * `export ACCESS_TOKEN_EXPIRE_MINUTES=30`
    * `export SQLALCHEMY_DB_URL='sqlite:///todo_app.db'`
5. Run uvicorn app.main:app from the TodoApp directory