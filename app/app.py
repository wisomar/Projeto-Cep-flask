from flask import Flask, render_template, request, flash, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para o uso de flash

BASE_URL = "https://viacep.com.br/ws/"

@app.route("/", methods=["GET", "POST"])
def consulta_cep():
    if request.method == "POST":
        cep = request.form.get("cep")
        if cep:
            try:
                # Faz a requisição para a API ViaCEP
                resposta = requests.get(f"{BASE_URL}{cep}/json", timeout=10)
                resposta.raise_for_status()
                dados = resposta.json()

                # Exibe o endereço, mesmo que os dados sejam incompletos
                if "erro" in dados:
                    flash("CEP não encontrado!", "error")
                else:
                    flash("Consulta realizada com sucesso!", "success")
                    return render_template("consulta_cep.html", endereco=dados)
            except requests.RequestException:
                flash("Erro ao consultar o CEP. Tente novamente.", "error")
        else:
            flash("Por favor, insira um CEP válido.", "error")

    return render_template("consulta_cep.html")

if __name__ == "__main__":
    app.run(debug=True)
