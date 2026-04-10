from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'qualquer'

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
