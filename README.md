# Architecture Web

Il est tout d'abord au préalable nécessaire d'avoir créé un environnement virtuel et d'avoir installer django.

### Installation des packages nécéssaire

Pour utiliser le site vous devez installer les packages requis :

    pip install -r requirement.txt

### Créer la base de données

Il est nécessaire de créer la base de données :

    python manage.py flush
    
Mettre yes

### Importer les fixtures

    python manage.py migrate

    python manage.py loaddata projet/fixtures/baseComplete.yaml 
    

### Démarrer le serveur

Il est fort conseillé pour une bonne utilisation du site de mettre la commande exact :

    python manage.py runserver localhost:8000

