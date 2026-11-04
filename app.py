from flask import Flask, render_template, redirect, request, url_for
import sqlite3
import base64
app = Flask(__name__)

@app.route("/")
def index():

    conn = conexao()
    categorias = conn.execute('SELECT * FROM categoria').fetchall()
    conn.close()
    return render_template("site/index.html", categorias = categorias)

@app.route("/admin")
def admin():
    return render_template("admin/base.html")


@app.route("/site")
def site():
    return redirect(url_for('index'))



def conexao():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/site/produtos/<int:id_categoria>")
def siteProdutos(id_categoria):

    conn = conexao()
    produtos = conn.execute(
        'SELECT * FROM produto WHERE id_categoria = ?',
        (id_categoria,)).fetchall()

    conn.close()

    return render_template('site/produtos.html', produtos = produtos)


@app.route("/listar_categorias")
def listarCategorias():
    conn = conexao()
    categoria = conn.execute('select * from categoria')
    return render_template("admin/listar_categoria.html", categoria = categoria)

@app.route("/cadastrar_categoria", methods=['GET', 'POST'])
def cadastrarCategoria():
    conn = conexao()

    if request.method =='POST':
        nome_categoria = request.form.get('nome_categoria')
        descricao = request.form.get('descricao')
        ativo = request.form.get('ativo')
        imagem = request.files.get('imagem')
        imagem_base64 = base64.b64encode(imagem.read()).decode('utf-8')
        if nome_categoria:
            conn = conexao()
            conn.execute('''INSERT INTO categoria (nome, descricao, ativo, imagem)
            VALUES (?, ?, ?, ?)''', (nome_categoria, descricao, ativo, imagem_base64))
            conn.commit()
            conn.close()
            return redirect(url_for('listarCategorias'))
        
    return render_template("admin/cadastrar_categoria.html")


@app.route("/editar_categoria/<int:id>", methods=['GET', 'POST'])
def editarCategoria(id):
    conn = conexao()
    categoria = conn.execute('select * from categoria where id=?', (id,)).fetchone()
    if request.method == 'POST':
        nome_categoria = request.form.get('nome_categoria')
        descricao = request.form.get('descricao')
        ativo = request.form.get('ativo')
        imagem = request.files.get('imagem')
        imagem_base64 = base64.b64encode(imagem.read()).decode('utf-8')
            
        if imagem:
            conn.execute(''' UPDATE categoria SET nome=?, descricao=?, ativo=?, imagem=? WHERE id=?''',
            (nome_categoria, descricao, ativo, imagem_base64, id))
            conn.commit()
            conn.close()

        else:
            conn.execute(''' UPDATE categoria SET nome=?, descricao=?, ativo=? WHERE id=?''',
            (nome_categoria, descricao, ativo, id))
            conn.commit()
            conn.close()

        return redirect(url_for('listarCategorias'))
            
    return render_template('admin/editar_categoria.html', categoria = categoria)

@app.route("/excluir_categoria/<int:id>", methods=['GET', 'POST'])
def excluirCategoria(id):
    conn = conexao()
    categoria = conn.execute(''' SELECT * FROM categoria WHERE id = ?''', (id,)).fetchone()

    if request.method == 'POST':
        conn.execute('DELETE FROM categoria WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('listarCategorias'))
    return render_template('admin/excluir_categoria.html', categoria = categoria)


@app.route("/listar_produtos")
def listarProdutos():
    conn = conexao()
    produto = conn.execute('''SELECT  produto.*, categoria.nome AS nome_categoria FROM produto 
    LEFT JOIN categoria ON produto.id_categoria = categoria.id''').fetchall()
    return render_template("admin/listar_produto.html", produto = produto)


@app.route("/cadastrar_produto", methods=('GET', 'POST'))
def cadastrarProduto():
    conn = conexao()
    categorias = conn.execute('SELECT * FROM categoria').fetchall()

    if request.method =='POST':
        nome_produto = request.form.get('nome_produto')
        preco_produto = request.form.get('preco_produto')
        ativo = request.form.get('ativo')
        id_categoria = request.form.get('categoria')
        imagem = request.files.get('imagem')
        imagem_base64 = base64.b64encode(imagem.read()).decode('utf-8')
        if nome_produto:
            conn = conexao()
            conn.execute('''INSERT INTO produto (nome, preco, ativo, id_categoria, imagem)
            VALUES (?, ?, ?, ?, ?)''', (nome_produto, preco_produto, ativo, id_categoria, imagem_base64))
            conn.commit()
            conn.close()
            return redirect(url_for('listarProdutos'))
        
    return render_template("admin/cadastrar_produto.html", categorias = categorias)


@app.route("/editar_produto/<int:id>", methods=['GET', 'POST'])
def editarProduto(id):
    conn = conexao()
    categorias = conn.execute('SELECT * FROM categoria').fetchall()
    produto = conn.execute('select * from produto where id=?', (id,)).fetchone()
    if request.method == 'POST':
        nome_produto = request.form.get('nome_produto')
        preco_produto = request.form.get('preco_produto')
        ativo = request.form.get('ativo')
        imagem = request.files.get('imagem')
        id_categoria = request.form.get('categoria')
        imagem_base64 = base64.b64encode(imagem.read()).decode('utf-8')
        
        if imagem:
            conn.execute(''' UPDATE produto SET nome=?, preco=?, ativo=?, id_categoria=?, imagem=? WHERE id=?''',
            (nome_produto, preco_produto, ativo, id_categoria, imagem_base64, id))
            conn.commit()
            conn.close()

        else:
            conn.execute(''' UPDATE produto SET nome=?, preco=?, ativo=?, id_categoria=?  WHERE id=?''',
            (nome_produto, preco_produto, ativo, id_categoria, id))
            conn.commit()
            conn.close()

        return redirect(url_for('listarProdutos'))
            
    return render_template('admin/editar_produto.html', produto = produto, categorias = categorias)


@app.route("/excluir_produto/<int:id>", methods=['GET', 'POST'])
def excluirProduto(id):
    conn = conexao()
    produto = conn.execute(''' SELECT * FROM produto WHERE id = ?''', (id,)).fetchone()

    if request.method == 'POST':
        conn.execute('DELETE FROM produto WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('listarProdutos'))
    
    return render_template('admin/excluir_produto.html', produto = produto)





app.run(debug=True, port=5000)
