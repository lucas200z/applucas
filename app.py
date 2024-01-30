from flask import Flask, render_template, request, jsonify
import pandas as pd

# Carregar o DataFrame do Excel
caminho_excel = 'PRODUTOS2024.xlsx'
df = pd.read_excel(caminho_excel)

# Inicializar o aplicativo Flask
app = Flask(__name__)

# Rota para fornecer sugestões com base no termo de pesquisa
# Rota para fornecer sugestões com base no termo de pesquisa
@app.route('/sugestoes')
def sugestoes():
    termo = request.args.get('termo', '').upper()

    # Verificar se a coluna 'PRODUTO' não tem valores nulos antes de aplicar o filtro
    if 'PRODUTO' in df.columns and not df['PRODUTO'].isnull().any():
        sugestoes_filtradas = df[df['PRODUTO'].str.upper().str.startswith(termo)]['PRODUTO'].tolist()
    else:
        sugestoes_filtradas = []

    return jsonify({'sugestoes': sugestoes_filtradas})


# Rota padrão
@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None

    # Verifica se o formulário foi submetido
    if request.method == 'POST':
        # Obtém os dados do formulário
        produto_desejado = request.form['produto'].upper()
        peso_balanca = float(request.form['peso_balanca'].replace(',', '.'))

        # Filtra o DataFrame para o produto desejado
        produto_df = df[df['PRODUTO'].str.upper() == produto_desejado]

        # Verifica se o produto foi encontrado
        if not produto_df.empty:
            # Obtém o valor do peso das embalagens na linha do produto desejado
            peso_das_embalagens = produto_df['PESO DAS EMBALAGEN'].values[0]

            # Calcula o peso sem embalagem (peso da balança - peso das embalagens)
            peso_sem_embalagem = peso_balanca - peso_das_embalagens

            # Obtém o valor do peso do litro sem embalagem na linha do produto desejado
            peso_litro_sem_embalagem = produto_df['PESO DO LITRO SEM EMBALAGEM'].values[0]

            # Verifica se o peso do litro sem embalagem é maior que zero
            if peso_litro_sem_embalagem != 0:
                # Calcula a quantidade de litros correspondente ao peso sem embalagem
                litros = peso_sem_embalagem / peso_litro_sem_embalagem

                # Formata o resultado
                resultado = f' {litros:.8f} litros '
            else:
                resultado = 'O valor de PESO DO LITRO SEM EMBALAGEM na tabela é zero ou não está disponível. Verifique os dados da tabela.'
        else:
            resultado = f'O produto {produto_desejado} não foi encontrado.'

    return render_template('index.html', resultado=resultado)

# Executa o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True)
