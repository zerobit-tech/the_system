rm -r venv

pip install --upgrade virtualenv
virtualenv venv --python=python3.9
source venv/bin/activate

python -m pip install --upgrade pip
cd sample_project/
pip install -r requirements.txt

cd ..

python setup.py sdist

cd sample_project/
python manage.py makemigrations
python manage.py migrate

git add .
git commit -m "Fix"
git push
python manage.py runserver 9021