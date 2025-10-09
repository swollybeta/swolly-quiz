from flask import Flask, request, session

app = Flask(__name__)
app.secret_key = "segredo_quiz_sneakers"

# Base de dados dos modelos e tags
sneakers = [
    {"name": "Jordan 1", "tags": ["OG", "colorful", "Jordan", "nike", "trendy", "basketball"]},
    {"name": "Jordan 4", "tags": ["trendy", "Jordan", "Costy", "niche"]},
    {"name": "Jordan 3", "tags": ["Jordan", "niche", "colorful", "OG"]},
    {"name": "Jordan 11", "tags": ["Jordan", "colorful", "OG", "basketball", "not popular"]},
    {"name": "Adidas Campus", "tags": ["adidas", "not nike", "skater", "trendy", "colorful"]}
]

def recommend_sneakers(user_tags, sneakers):
    recommendations = []
    for sneaker in sneakers:
        common = set(user_tags) & set(sneaker["tags"])
        recommendations.append({
            "name": sneaker["name"],
            "match_count": len(common),
            "tags": list(common)
        })
    recommendations.sort(key=lambda x: x["match_count"], reverse=True)
    return recommendations

@app.route('/', methods=['GET', 'POST'])
def quiz1():
    if request.method == 'POST':
        escolha = request.form.get('esporte')
        user_tags = []
        if escolha == "basketball":
            user_tags.append("basketball")
        elif escolha == "skate":
            user_tags.append("skater")
        session['user_tags'] = user_tags
        return '''
            <form method="POST" action="/q2">
                <h2>Preferes sapatilhas famosas ou desconhecidas?</h2>
                <input type="radio" name="fama" value="famosas"> Famosas<br>
                <input type="radio" name="fama" value="desconhecidas"> Desconhecidas<br>
                <button type="submit">Enviar</button>
            </form>
        '''
    return '''
        <form method="POST">
            <h2>Preferes basketball ou skate?</h2>
            <input type="radio" name="esporte" value="basketball"> Basketball<br>
            <input type="radio" name="esporte" value="skate"> Skate<br>
            <button type="submit">Enviar</button>
        </form>
    '''

@app.route('/q2', methods=['POST'])
def quiz2():
    escolha_fama = request.form.get('fama')
    user_tags = session.get('user_tags', [])
    if escolha_fama == "famosas":
        user_tags.append("trendy")
    elif escolha_fama == "desconhecidas":
        user_tags.append("not popular")
    session['user_tags'] = user_tags
    return '''
        <form method="POST" action="/q3">
            <h2>Gostas de sapatilhas com muitas cores?</h2>
            <input type="radio" name="cores" value="sim"> Sim<br>
            <input type="radio" name="cores" value="nao"> Não<br>
            <button type="submit">Enviar</button>
        </form>
    '''

@app.route('/q3', methods=['POST'])
def quiz3():
    escolha_cores = request.form.get('cores')
    user_tags = session.get('user_tags', [])
    if escolha_cores == "sim":
        user_tags.append("colorful")
    # se "não" não adiciona tag
    session['user_tags'] = user_tags
    return '''
        <form method="POST" action="/q4">
            <h2>Preferes Nike ou Jordan?</h2>
            <input type="radio" name="marca" value="nike"> Nike<br>
            <input type="radio" name="marca" value="jordan"> Jordan<br>
            <button type="submit">Enviar</button>
        </form>
    '''

@app.route('/q4', methods=['POST'])
def quiz4():
    escolha_marca = request.form.get('marca')
    user_tags = session.get('user_tags', [])
    if escolha_marca == "nike":
        user_tags.append("nike")
    elif escolha_marca == "jordan":
        user_tags.append("Jordan")
        user_tags.append("not nike")
    session['user_tags'] = user_tags
    # Recomendar sapatilha
    recomendados = recommend_sneakers(user_tags, sneakers)
    melhor = recomendados[0]
    return f"<h2>Modelo recomendado:</h2><b>{melhor['name']}</b><br><br>Tags coincidentes: {', '.join(melhor['tags'])}"

if __name__ == '__main__':
    app.run(debug=True)