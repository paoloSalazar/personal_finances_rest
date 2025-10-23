# My Daily Finances REST API
## File Structure

personal_finances_rest
├── README.md
├── api.rest
├── data
│   ├── __init__.py
│   ├── category.py
│   └── init.py
├── db
│   └── personal_finances.db
├── fake
│   ├── __init__.py
│   └── category.py
├── main.py
├── model
│   ├── __init__.py
│   └── category.py
├── pyproject.toml
├── requirements.txt
├── service
│   ├── __init__.py
│   └── category.py
├── test
│   ├── __init__.py
│   └── unit
│       └── service
│           └── test_category.py
└── web
    ├── __init__.py
    └── category.py

* main.py is the main file in which the start of the project is setup
* web folder: rest api end points
* service: project logic 
* model: database models
* data: database setup
