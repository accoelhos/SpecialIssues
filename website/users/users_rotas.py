# user_routes.py
# aqui estão as rotas de um usuário comum (Não admin)
# esse usuário comum só tem acesso a home, detalhes e busca

from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from website import db, app
from website.adm.models import SPI

#pagina inicial de usuario
@app.route('/')
def home():
    per_page = 10
    page = request.args.get('page', type=int, default=1)
    specialissues = SPI.query.order_by(SPI.prazo.asc()).paginate(page=page, per_page=per_page)
    return render_template('users/users_home.html', title='Home para Usuários', specialissues=specialissues)

#detalhes das si 
@app.route('/detalhes/<int:id>', methods=['GET'])
def users_detalhes(id):
    
    spi = SPI.query.get(id)
    if spi:
        return render_template('users/users_detalhes.html', spi=spi, title='Detalhes da Special Issue')
    else:
        flash('Special Issue não encontrado', 'danger')
        return redirect(url_for('user.home'))

#busca de user
@app.route('/search', methods=['GET', 'POST'])
def users_search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search-box']
        # Redireciona para a rota GET com o valor da busca na URL
        return redirect(url_for('users_search', search_value=search_value))
    
    # Para requisições GET
    search_value = request.args.get('search_value', '')  # Obtém o valor da busca da URL
    page = request.args.get('page', 1, type=int)
    per_page = 20

    if search_value:
        specialissues = SPI.query.filter(
            SPI.titulo.like(f"%{search_value}%") | SPI.detalhes.like(f"%{search_value}%")
        ).paginate(page=page, per_page=per_page)
    else:
        specialissues = SPI.query.paginate(page=page, per_page=per_page)

    return render_template('users/users_busca.html', specialissues=specialissues, search_value=search_value)

