# GET Search cafe by location

http://127.0.0.1:5000/search?loc=Peckhaall

/search route will search the cafe by matching the loc parameter

<img width="342" alt="image" src="https://github.com/Prashanna-Raj-Pandit/REST-API-demo-project/assets/108394628/39a2a38b-b53f-4092-8022-7a93c17dd01c">

# DELETE Delete a cafe by ID

http://127.0.0.1:5000/report-closed/7?api_key=YOUR_SECRET_API_KEY

Delete a cafe data by using a route /report-closed/CAFE_ID?api_kay=YOUR_API_KEY

<img width="411" alt="image" src="https://github.com/Prashanna-Raj-Pandit/REST-API-demo-project/assets/108394628/8cc9a298-762d-4fa8-afb7-0e5d75b72f2b">

# GET Get all cafes

http://127.0.0.1:5000/all

Get all cafe by requesting a route /all


# GET Get a random cafe

http://127.0.0.1:5000/random

# Get a random cafe near you by requesting a route /random

PATCH Update the price of cafe

http://127.0.0.1:5000/update-price/70?new_price=350

<img width="411" alt="image" src="https://github.com/Prashanna-Raj-Pandit/REST-API-demo-project/assets/108394628/1787519a-9f21-4f24-809d-48d5849adbed">

## Step-by-step execution flow

1. Python starts executing main.py

2. from app import create_app
* Python loads the app/ package
* This triggers execution of app/__init__.py

3. Imports inside app/__init__.py are evaluated
```
from .config import DevConfig
from .extensions import db, migrate
from .routes import api
```
This results in:

* config.py loading configuration classes

* extensions.py creating unbound extension objects:
```commandline
db = SQLAlchemy()
migrate = Migrate()
```
* routes.py defining:
```commandline
api = Blueprint(...)
```
along with all @api.route(...) endpoint definitions

At this stage:

* Blueprints and routes are defined
* No Flask application instance exists yet

4. create_app() is called in main.py

```commandline
app = create_app()
```
5. Inside create_app()

* (i) Create the Flask application
```commandline
app = Flask(__name__)
```
* (ii) Load configuration
```commandline
app.config.from_object(DevConfig)

```
* Copies all uppercase configuration attributes from DevConfig into app.config

* (iii) Initialize extensions
```commandline
db.init_app(app)
```

* (iv) Register blueprints

```commandline
app.register_blueprint(api)
```
* Copies all routes defined in the blueprint into the application’s routing table

* (v) Return the fully configured app

```commandline
return app
```

6. Back in main.py
```commandline
app.run()
```
* Starts the Flask development server
* The app is now ready to handle incoming requests

## B) When a request is received (example: GET /random)

1. The browser sends a request to /random
2. Flask checks the application’s routing table (app.url_map)
3. It finds the endpoint registered from the blueprint (e.g., api.get_random_cafe)
4. Flask calls the corresponding Python function
5. The function returns a response (JSON or HTML)
6. Flask converts the return value into an HTTP response and sends it back to the client


```commandline
main.py
  ↓
create_app()
  ↓
Flask app created
  ↓
config loaded
  ↓
db initialized
  ↓
migrations attached
  ↓
routes registered
  ↓
app.run()

```