# SocialMetrics AI - API d'Analyse de Sentiments

#### Membres du groupe :

1. Ali LOUDAGH
2. Nahel KINI
3. Roman SABECHKINE
4. Gregoire LEQUIPPE

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
    "That's crap!",
    "The worst ever.",
    "Amazing experience!",
    "Not bad, but not great.",
    "eww so disgusting",
    "bad",
    "horrible!",
    "very nice"
  ]
}
```

**Réponse** :

```json
{
  "Amazing experience!": 0.03,
  "I love this!": 0.22,
  "Not bad, but not great.": -0.38,
  "That's crap!": -0.03,
  "The worst ever.": -0.17,
  "bad": -0.31,
  "eww so disgusting": -0.19,
  "horrible!": -0.26,
  "very nice": 0.15
}
```

---

## Réentraîner le Modèle

Pour vérifier que le cronjob fonctionne correctement, vous pouvez consulter les logs du conteneur qui gère le
réentraînement automatique :

```bash
docker-compose logs -f flask-app
```

### Étape 1 : Modifier les données d'entraînement

Ajoutez plus de tweets à la table `tweets` de la base de données pour améliorer le modèle.

### Étape 2 : Lancer le script de réentraînement

Si vous souhaitez réentraîner le modèle avec de nouvelles données :

```bash
docker exec -it flask-app python /app/retrain.py
```

Vous devriez voir un message indiquant que le réentraînement a été effectué, comme : *Model retrained successfully.*

Cela signifie que le réentraînement a été effectué avec succès.

### Étape 3 : cron pour un réentraînement automatique

Pour vérifier que le cronjob fonctionne correctement :

```bash
docker exec -it flask-app service cron status
```

Vous devriez voir un message indiquant : *cron is running*

Cela signifie que le setup du cron marche.

Vérifiez si la tâche cron est planifiée à l'intérieur du conteneur :

```bash
docker exec -it flask-app crontab -l
```

Vous devriez voir un message indiquant : *0 0 * * 0 python /app/retrain.py >> /var/log/cron.log 2>&1*

## Tests

Une fois le serveur lancé via Docker Compose, vous pouvez tester l'API en envoyant des requêtes POST via **Postman** ou
**curl**.

```bash
curl -X POST http://127.0.0.1:5000/analyze -H "Content-Type: application/json" -d '{"tweets": ["I love this!", "That's crap!"]}'
```

---
