import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import statistics
from collections import Counter

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ─── MODEL ───────────────────────────────────────────────────────────────────

class Response(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    pseudo        = db.Column(db.String(80), nullable=False)
    age_group     = db.Column(db.String(20), nullable=False)   # <18, 18-25, 26-35, 36-50, 50+
    country       = db.Column(db.String(80), nullable=False)
    fav_song      = db.Column(db.String(120), nullable=False)
    fav_era       = db.Column(db.String(80), nullable=False)   # Jackson 5, Off the Wall, Thriller, Bad, Dangerous, HIStory
    rating        = db.Column(db.Integer, nullable=False)      # 1-10
    listens_week  = db.Column(db.Integer, nullable=False)      # nb écoutes/semaine
    emotion       = db.Column(db.String(40), nullable=False)   # Joy, Nostalgia, Energy, Sadness, Inspiration
    submitted_at  = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# ─── ROUTES ──────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/dashboard')
def dashboard():
    return app.send_static_file('dashboard.html')

@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Données JSON invalides'}), 400

    required = ['pseudo','age_group','country','fav_song','fav_era','rating','listens_week','emotion']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'Champ manquant : {field}'}), 400

    r = Response(
        pseudo       = data['pseudo'][:80],
        age_group    = data['age_group'],
        country      = data['country'][:80],
        fav_song     = data['fav_song'],
        fav_era      = data['fav_era'],
        rating       = max(1, min(10, int(data['rating']))),
        listens_week = max(0, min(9999, int(data['listens_week']))),
        emotion      = data['emotion'],
    )
    db.session.add(r)
    db.session.commit()
    return jsonify({'success': True, 'id': r.id}), 201

@app.route('/api/stats')
def stats():
    rows = Response.query.all()
    if not rows:
        return jsonify({'count': 0})

    ratings       = [r.rating for r in rows]
    listens       = [r.listens_week for r in rows]
    songs         = [r.fav_song for r in rows]
    eras          = [r.fav_era for r in rows]
    emotions      = [r.emotion for r in rows]
    age_groups    = [r.age_group for r in rows]
    countries     = [r.country for r in rows]

    def freq(lst):
        c = Counter(lst)
        total = len(lst)
        return [{'label': k, 'count': v, 'pct': round(v/total*100,1)} for k,v in c.most_common()]

    # Moyenne rating par chanson
    song_ratings = {}
    for r in rows:
        song_ratings.setdefault(r.fav_song, []).append(r.rating)
    avg_by_song = [{'song': s, 'avg': round(statistics.mean(v),2), 'count': len(v)}
                   for s, v in sorted(song_ratings.items(), key=lambda x: -statistics.mean(x[1]))]

    # Distribution des notes (histogramme)
    hist = Counter(ratings)
    rating_dist = [{'note': i, 'count': hist.get(i, 0)} for i in range(1, 11)]

    return jsonify({
        'count'         : len(rows),
        'rating_mean'   : round(statistics.mean(ratings), 2),
        'rating_median' : statistics.median(ratings),
        'rating_mode'   : Counter(ratings).most_common(1)[0][0],
        'listens_mean'  : round(statistics.mean(listens), 2),
        'songs'         : freq(songs),
        'eras'          : freq(eras),
        'emotions'      : freq(emotions),
        'age_groups'    : freq(age_groups),
        'countries'     : freq(countries)[:10],
        'avg_by_song'   : avg_by_song,
        'rating_dist'   : rating_dist,
        'last_5'        : [{'pseudo': r.pseudo, 'song': r.fav_song, 'rating': r.rating,
                            'country': r.country, 'at': r.submitted_at.strftime('%d/%m %H:%M')}
                           for r in rows[-5:][::-1]],
    })

@app.route('/api/count')
def count():
    return jsonify({'count': Response.query.count()})

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)