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

### Finalisation

Site fonctionnel.

### Quelques remarques

* Base de données
..* Une vingtaine de comptes ont été créé afin que le site soit testable malgré cette petite base de données.
..* Notre base de données est ciblée sur les Pays de la Loire mais susceptible de contenir des informations de la France entière. 

* Mot de passe oublié
..* L'envoi du mail indiquant le nouveau mot de passe en cas d'oublie est généré dans le terminal afin d'empêcher l'envoi de réel mail.

* Chat entre affinités
..* Le chat entre deux affinités doit être actualisé via le bouton "Acutaliser". Les messages ne sont pas rechargés automatiquement à interval de temps régulier.


