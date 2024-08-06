# Django Pokedex

## Setup

### Clone the Repo

Clone the repository.
```bash
git clone https://github.com/geraldsaberon/django-pokedex.git
```
and then cd inside.
```bash
cd django-pokedex
```

### Create Python Virtual Environment
```bash
python -m venv venv
```
Then activate virtual environment

Using Bash:
```bash
source venv/Scripts/activate
```
Using Windows cmd:
```
venv\Scripts\activate.bat
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Django Migrations
```bash
python manage.py migrate
```

### Populate Pokedex Database
```bash
python manage.py populatepokedex
```

### Run Dev Server
```bash
python manage.py runserver
```
And then go to [http://127.0.0.1:8000/pokedex/](http://127.0.0.1:8000/pokedex/) or [http://127.0.0.1:8000/](http://127.0.0.1:8000/) 
