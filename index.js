// Particles
        const pc = document.getElementById('particles');
        for (let i = 0; i < 30; i++) {
            const p = document.createElement('div');
            p.className = 'particle';
            p.style.cssText = `left:${Math.random() * 100}%;animation-duration:${6 + Math.random() * 10}s;animation-delay:${Math.random() * 8}s;--dx:${(Math.random() - 0.5) * 100}px`;
            pc.appendChild(p);
        }

        // Stars rating
        let currentRating = 0;
        const stars = document.querySelectorAll('.star');
        const ratingVal = document.getElementById('rating-val');

        stars.forEach(s => {
            s.addEventListener('mouseover', () => highlightStars(+s.dataset.v));
            s.addEventListener('mouseout', () => highlightStars(currentRating));
            s.addEventListener('click', () => { currentRating = +s.dataset.v; highlightStars(currentRating); });
        });

        function highlightStars(n) {
            stars.forEach(s => s.classList.toggle('active', +s.dataset.v <= n));
            ratingVal.textContent = n || '—';
        }

        // Emotion pills
        let currentEmotion = '';
        document.querySelectorAll('.emotion-pill').forEach(p => {
            p.addEventListener('click', () => {
                document.querySelectorAll('.emotion-pill').forEach(x => x.classList.remove('selected'));
                p.classList.add('selected');
                currentEmotion = p.dataset.v;
            });
        });

        // Counter
        fetch('/api/count').then(r => r.json()).then(d => {
            document.getElementById('hero-count').textContent = d.count;
        });

        // Submit
        async function submitForm() {
            const payload = {
                pseudo: document.getElementById('pseudo').value.trim(),
                age_group: document.getElementById('age_group').value,
                country: document.getElementById('country').value.trim(),
                fav_song: document.getElementById('fav_song').value,
                fav_era: document.getElementById('fav_era').value,
                rating: currentRating,
                listens_week: document.getElementById('listens_week').value,
                emotion: currentEmotion,
            };

            const errEl = document.getElementById('error-msg');
            const btn = document.getElementById('btn-submit');

            if (!payload.pseudo || !payload.age_group || !payload.country ||
                !payload.fav_song || !payload.fav_era || !currentRating ||
                !payload.listens_week || !currentEmotion) {
                errEl.style.display = 'block';
                return;
            }
            errEl.style.display = 'none';

            btn.disabled = true;
            btn.textContent = '⏳  Envoi en cours…';

            try {
                const res = await fetch('/api/submit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (data.success) {
                    document.getElementById('success').classList.add('show');
                } else {
                    alert('Erreur : ' + (data.error || 'Inconnue'));
                    btn.disabled = false;
                    btn.textContent = '🎤  Soumettre ma réponse';
                }
            } catch (e) {
                alert('Erreur réseau. Vérifiez que le serveur tourne.');
                btn.disabled = false;
                btn.textContent = '🎤  Soumettre ma réponse';
            }
        }

        function resetForm(e) {
            e.preventDefault();
            document.getElementById('success').classList.remove('show');
            document.getElementById('pseudo').value = '';
            document.getElementById('country').value = '';
            document.getElementById('listens_week').value = '';
            document.getElementById('age_group').value = '';
            document.getElementById('fav_song').value = '';
            document.getElementById('fav_era').value = '';
            currentRating = 0; highlightStars(0);
            currentEmotion = '';
            document.querySelectorAll('.emotion-pill').forEach(p => p.classList.remove('selected'));
            document.getElementById('btn-submit').disabled = false;
            document.getElementById('btn-submit').textContent = '🎤  Soumettre ma réponse';
        }