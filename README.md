# MJ Legacy — Sondage Musical

> Travaux Pratiques (TP) — Unité d'Enseignement **INF 232**

---

## Informations académiques

| Champ         | Valeur                              |
|---------------|-------------------------------------|
| **Étudiant**  | TIETCHAK TIAGO ESTHERA JOANNA       |
| **Matricule** | 24F2810                             |
| **Enseignant**| *(Nom du professeur)*               |
| **UE**        | INF 232                             |
| **Type**      | Travaux Pratiques (TP)              |

---

## Description du projet

**MJ Legacy** est une application web de collecte et d'analyse de données musicales centrée sur l'artiste **Michael Jackson**. Elle permet à des utilisateurs de soumettre leurs préférences musicales via un formulaire interactif, et visualise en temps réel les résultats agrégés sur un tableau de bord analytique.

Ce projet illustre les concepts de développement web full-stack : conception d'une API REST avec Python/Flask, gestion d'une base de données avec SQLAlchemy, et rendu de données dynamiques côté client avec JavaScript et Chart.js.

---

## Fonctionnalités

### Formulaire de sondage (`/`)
- Saisie du pseudo et de la tranche d'âge
- Sélection du pays d'origine
- Choix de la chanson préférée parmi une liste prédéfinie
- Choix de l'ère / album préféré (Jackson 5, Thriller, Bad, etc.)
- Notation globale de 1 à 10 via un système d'étoiles interactif
- Indication du nombre d'écoutes par semaine
- Sélection de l'émotion ressentie à l'écoute de MJ
- Validation des champs côté client avant envoi
- Affichage d'un message de succès animé après soumission

### Tableau de bord analytique (`/dashboard`)
- Nombre total de réponses enregistrées
- Note moyenne, médiane et mode
- Graphiques interactifs (Chart.js) :
  - Chansons les plus appréciées
  - Ères / Albums préférés
  - Émotions ressenties
  - Répartition par tranche d'âge
  - Distribution des notes (histogramme)
  - Note moyenne par chanson
  - Top 10 des pays représentés
- Tableau des 5 dernières réponses soumises
- Actualisation en temps réel via bouton

---

inf232/
├── app.py          # Backend Flask (API REST + serveur de fichiers statiques)
├── index.html      # Page du formulaire de sondage
├── index.js        # Logique frontend (formulaire, étoiles, émotions, soumission)
├── style.css       # Styles de la page formulaire
├── dashboard.html  # Page du tableau de bord
├── dashboard.css   # Styles du tableau de bord
├── vercel.json     # Configuration de déploiement sur Vercel
├── requirements.txt # Dépendances Python pour Vercel
└── instance/
    └── mjsurvey.db # Base de données SQLite (générée automatiquement)

### Stack technologique

| Couche      | Technologie                          |
|-------------|--------------------------------------|
| Backend     | Python 3, Flask, Flask-SQLAlchemy, Flask-CORS |
| Base de données | SQLite (via SQLAlchemy ORM)     |
| Frontend    | HTML5, CSS3, JavaScript (Vanilla)    |
| Graphiques  | Chart.js (CDN)                       |
| Typographie | Google Fonts (Bebas Neue, DM Sans)   |

---

## API REST

| Méthode | Route          | Description                                  |
|---------|----------------|----------------------------------------------|
| `GET`   | `/`            | Sert la page du formulaire                   |
| `GET`   | `/dashboard`   | Sert la page du tableau de bord              |
| `POST`  | `/api/submit`  | Enregistre une nouvelle réponse (JSON)       |
| `GET`   | `/api/stats`   | Retourne les statistiques agrégées (JSON)    |
| `GET`   | `/api/count`   | Retourne le nombre total de réponses (JSON)  |

### Exemple de payload `/api/submit`

```json
{
  "pseudo": "Cutedev",
  "age_group": "18-25",
  "country": "Cameroun",
  "fav_song": "Billie Jean",
  "fav_era": "Thriller",
  "rating": 9,
  "listens_week": 7,
  "emotion": "Nostalgia"
}
```

---

## Installation et lancement

### Prérequis
- Python 3.10+

### Étapes

```bash
# 1. Cloner ou télécharger le projet
cd inf232

# 2. Créer un environnement virtuel
python3 -m venv venv

# 3. Activer l'environnement virtuel
source venv/bin/activate

# 4. Installer les dépendances
pip install flask flask-sqlalchemy flask-cors

# 5. Lancer le serveur
python3 app.py
```

L'application sera disponible à l'adresse : **http://127.0.0.1:5000**

---

## Modèle de données

La table `response` (SQLite) contient les colonnes suivantes :

| Colonne        | Type        | Description                          |
|----------------|-------------|--------------------------------------|
| `id`           | Integer (PK)| Identifiant unique                   |
| `pseudo`       | String(80)  | Pseudo ou prénom de l'utilisateur    |
| `age_group`    | String(20)  | Tranche d'âge                        |
| `country`      | String(80)  | Pays de l'utilisateur                |
| `fav_song`     | String(120) | Chanson préférée                     |
| `fav_era`      | String(80)  | Ère / Album préféré                  |
| `rating`       | Integer     | Note globale (1–10)                  |
| `listens_week` | Integer     | Nombre d'écoutes par semaine         |
| `emotion`      | String(40)  | Émotion ressentie                    |
| `submitted_at` | DateTime    | Date et heure de soumission          |

---

*Projet réalisé dans le cadre de l'UE INF 232 — Développement Web.*
