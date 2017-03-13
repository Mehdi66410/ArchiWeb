# Architecture Web

Il est tout d'abord nécessaire de créer son environnement virtuel.

### Créer son environnement virtuel

Placez-vous à la racine de votre compte en faisant :

    cd

Ensuite, créez votre environnement virtuel :

    virtualenv -p /usr/bin/python3 env_archi

Vérifiez que l'environnement a bien été créé :

    ls -al env_archi/

Pour pouvoir l'utiliser, vous allez devoir l'activer à chaque fois que vous vous connecterez sur `mordor` comme ceci :

    source env_archi/bin/activate

Votre prompt devrait avoir changé et il devrait être préfixé par `(env_archi)` comme ceci :

    (env_archi):~$

### Installer django

Maintenant que vous avez activé votre environnement virtuel (votre prompt **DOIT** etre préfixé par (env_archi), vous pouvez installer `Django` :

    pip install Django

Ça devrait vous afficher comme dernière ligne :

    Successfully installed Django-1.10.5

Vérifiez que c'est bien le cas avec cette commande :

    python -c "import django; print(django.get_version())"

### Créer la base de données

Il est nécessaire de créer la base de données :

    python manage.py flush
    
Mettre yes

### Importer les fixtures

    python manage.py makemigrations socialnetwork

    python manage.py loaddata projet/fixtures/baseComplete.yaml 
    
    python manage.py migrate

### Démarrer le serveur

Il est fort conseillé pour une bonne utilisation du site de mettre la commande exact :

    python manage.py runserver localhost:8000

