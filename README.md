# Architecture Web

Il est tout d'abord au préalable nécessaire d'avoir créé un environnement virtuel et d'avoir installé django.

### Installation des packages nécéssaire

Pour utiliser le site vous devez installer les packages requis dans le dossier de l'environnement virtuel:

    pip install -r requirements.txt

### Créer la base de données

Il est nécessaire de créer la base de données :

    python manage.py makemigrations socialnetwork
    
    python manage.py sqlmigrate socialnetwork 0001
    
    python manage.py migrate
    
Mettre yes

### Importer les fixtures


    python manage.py loaddata projet/fixtures/baseComplete.yaml 
    

### Démarrer le serveur

Il est fort conseillé pour une bonne utilisation du site de mettre la commande exact :

    python manage.py runserver localhost:8000

