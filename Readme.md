# For Starting the Project First create virtual environment

python -m venv venv

# After that activate the virtual environment

venv/Scripts/activate

# Then install the requirements from r.txt

pip install -r r.txt

# After that make migrations

python manage.py makemigrations

# Then migrate 

python maange.py migrate

# After that run the server

python maange.py runserver