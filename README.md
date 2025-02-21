# SocialMetrics AI - API d'Analyse de Sentiments

## Prérequis

Avant de commencer, assurez-vous d'avoir installé Docker et Docker Compose.

- Docker : [Installation Docker](https://www.docker.com/get-started)
- Docker Compose : [Installation Docker Compose](https://docs.docker.com/compose/install/)

## Installation

### Étape 1 : Clonez le dépôt
```bash
git clone https://github.com/tactics177/SocialMetricsAI.git
cd SocialMetricsAI
```

### Étape 2 : Lancer Docker Compose
Dans le dossier du projet, lancez les services Flask et MySQL via Docker Compose :
```bash
docker-compose up --build
```

Cette commande va :
- Construire l'image Docker pour l'application Flask.
- Lancer MySQL dans un conteneur Docker.
- Démarrer l'application Flask, accessible sur `http://127.0.0.1:5000`.

### Étape 3 : Vérifiez que les services fonctionnent
Accédez à `http://127.0.0.1:5000` pour vérifier que l'API est bien en cours d'exécution.

---

## Utilisation de l'API

### Endpoint : `/analyze`

**Méthode** : POST  
**Paramètres** : JSON avec une clé `tweets` qui contient une liste de tweets à analyser.

#### Exemple de requête :
```json
{
  "tweets": [
    "I love this!",
    "That's crap!"
  ]
}
```

**Réponse** :
```json
{
  "I love this!": 0.5,
  "That's crap!": -0.8
}
```

---

## Réentraîner le Modèle

Pour vérifier que le cronjob fonctionne correctement, vous pouvez consulter les logs du conteneur qui gère le réentraînement automatique :

bash
docker-compose logs -f flask-app

### Étape 1 : Modifier les données d'entraînement
Ajoutez plus de tweets à la table `tweets` de la base de données pour améliorer le modèle.

### Étape 2 : Lancer le script de réentraînement
Si vous souhaitez réentraîner le modèle avec de nouvelles données :
```bash
docker-compose exec flask-app python retrain.py
```

### Étape 3 : cron pour un réentraînement automatique 

Pour vérifier que le cronjob fonctionne correctement, vous pouvez consulter les logs du conteneur qui gère le réentraînement automatique :

bash
docker-compose logs -f flask-app
Vous devriez voir un message indiquant que le réentraînement a été effectué, comme :
Modèle réentrainé
Cela signifie que le réentraînement a été effectué avec succès.

## Tests

Une fois le serveur lancé via Docker Compose, vous pouvez tester l'API en envoyant des requêtes POST via **Postman** ou **curl**.

```bash
curl -X POST http://127.0.0.1:5000/analyze -H "Content-Type: application/json" -d '{"tweets": ["I love this!", "That's crap!"]}'
```

---
