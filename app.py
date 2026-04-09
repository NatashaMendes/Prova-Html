from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'qualquer'

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    # methods=['GET', 'POST'] informa ao Flask que esta rota aceita AMBOS os métodos.
    # GET: exibe o formulário vazio (quando o usuário chega na página).
    # POST: processa os dados enviados (quando o usuário clica em "Enviar").
    # Sem essa declaração, Flask aceita apenas GET por padrão.

    if request.method == 'POST':
        # Este bloco só executa quando o formulário foi enviado (método POST).

        # request.form é um dicionário com todos os campos do formulário.
        # A chave é o atributo 'name' do campo HTML.
        nome = request.form['nome']
        email = request.form['email']
        cidade = request.form['cidade']

        # Por enquanto apenas imprimimos no terminal — banco de dados vem na Aula 05.
        print(f'Novo cadastro recebido: {nome} | {email} | {cidade}')

        # flash() envia uma mensagem de feedback para o próximo template renderizado.
        flash(f'Cadastro de {nome} realizado com sucesso!', 'success')

        # redirect() + url_for() redireciona para outra rota após processar o POST.
        # Este padrão (POST → redirect → GET) é chamado de PRG pattern e evita
        # que o navegador reenvie o formulário ao recarregar a página.
        return redirect(url_for('pagina_inicial'))

    # Se o método for GET (ou seja, se chegamos aqui sem ser por POST):
    # apenas renderizamos o formulário vazio.
    return render_template('cadastro.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/resultados')
def resultados():
    calculos = session.get('calculos', [])

    return render_template('resultados.html', calculos=calculos, total=len(calculos))

@app.route('/calcular', methods=['GET', 'POST'])
def calcular():

    if request.method =='POST':
        nome = request.form.get('nome', 'Não achei porcaria nenhuma')
        distancia = request.form.get('distancia', 'Não achei porcaria nenhuma')
        consumo = request.form.get('consumo', 'Não achei porcaria nenhuma')
        preco_comb = request.form.get('preco_comb', 'Não achei porcaria nenhuma')
        custo_total = request.form.get('custo_total', 'Não achei porcaria nenhuma')
        custo_rodado = request.form.get('custo_rodado', 'Não achei porcaria nenhuma')

        quant_litros = round(float(distancia) + (float(consumo) ),2)
        
        if quant_litros < 8:
            classificacao = 'Beberrao'

        elif quant_litros <= 15:
            classificacao = 'Padrão'

        elif quant_litros < 18:
            classificacao = 'Econômico'

        elif quant_litros > 18:
            classificacao = 'Super Economico'

        else:
            classificacao = 'Deu erro na conta!'

        flash(f'quant_litros: {quant_litros} - Classificação: {classificacao}', 'success')

        #armazenar session
        novo_calculo = {
            'nome': nome,
            'distancia' : distancia,
            'consumo' : consumo,
            'quant_litros' : quant_litros,
            'preco_comb' : preco_comb,
            'custo_total' : custo_total,
            'custo_rodado' : custo_rodado,
            'classificacao' : classificacao

        }

        #verifica se existe calculos na session
        if 'calculos' not in session:
            session ['calculos'] = []

        #adiciona o calculos na session
        session['calculos'].append(novo_calculo)

        session.modified = true # avisa que a session mudou


        return redirect(url_for('resultados'))



    return render_template('formulario.html')



if __name__ == '__main__':
    app.run(debug=True)
