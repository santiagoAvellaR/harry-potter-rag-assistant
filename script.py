import sys
import re

file_path = 'c:/Users/iagor/Documents/UTC/GI04/LO17/RAG/local/presentation/presentation.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Split the content at the start of old Slide 3
split_point = '<!-- Slide 3: Vue d\'ensemble du RAG -->'
parts = content.split(split_point)
if len(parts) != 2:
    print('Error: Could not find Slide 3 start.')
    sys.exit(1)

pre_content = parts[0]
post_content = split_point + parts[1]

# Now, in the post_content, shift all slide numbers from 9 down to 3
for i in range(9, 2, -1):
    post_content = post_content.replace(f'<!-- Slide {i}:', f'<!-- Slide {i+1}:')
    post_content = post_content.replace(f'id="slide{i}"', f'id="slide{i+1}"')
    post_content = post_content.replace(f'LO17 - Slide {i}</span>', f'LO17 - Slide {i+1}</span>')

# Update the 1 / 9 indicator to 1 / 10
post_content = post_content.replace('1 / 9', '1 / 10')
# In case the js has totalSlides = slides.length, it's dynamic. So we don't need to change JS.

new_slide = '''<!-- Slide 3: Moteur de Recherche Standard -->
            <div class="slide" id="slide3">
                <div class="slide-content">
                    <div class="slide-header">
                        <span class="slide-tag">SRI Classique</span>
                        <h2 class="slide-title">Le Moteur de Recherche Standard</h2>
                    </div>
                    <div class="slide-body">
                        <div class="grid-2">
                            <div class="card">
                                <div class="card-title">🔍 Comment ça marche ?</div>
                                <p>Un moteur classique fonctionne par mots-clés stricts (ex: requêtes booléennes). L'utilisateur soumet des mots et le système retourne les documents qui les contiennent exactement.</p>
                                <ul>
                                    <li><strong>Méthode :</strong> Indexation par mots-clés, TF-IDF, BM25.</li>
                                    <li><strong>Exemple :</strong> <code>baguette AND (sureau OR houx)</code></li>
                                </ul>
                            </div>
                            <div class="card">
                                <div class="card-title">⚠️ Les Limites du Standard</div>
                                <p>C'est face à ces limites que naît le besoin d'un système intelligent (RAG) :</p>
                                <ul style="gap: 0.6rem; display: flex; flex-direction: column;">
                                    <li><strong style="color:#ff6b6b">Aucune compréhension du sens :</strong> "Ollivander" et "fabricant de baguettes" sont deux concepts isolés pour un moteur classique.</li>
                                    <li><strong style="color:#ff6b6b">Pas de réponse directe :</strong> Le système retourne des <em>documents</em>, pas des réponses. L'utilisateur doit fouiller et lire les textes lui-même pour trouver l'information.</li>
                                    <li><strong style="color:var(--accent-purple)">La Solution :</strong> Combiner la recherche (Retrieval) avec l'intelligence de synthèse (Generation).</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="slide-footer">
                        <span class="utc-logo">UTC</span>
                        <span>LO17 - Slide 3</span>
                    </div>
                </div>
            </div>

            '''

new_content = pre_content + new_slide + post_content

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Success: Shifted slides and added new Slide 3.')
