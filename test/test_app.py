import pytest
from flask import Flask
from app.app import app  # Certifique-se de que o nome do arquivo Python é app.py ou ajuste o import
from pytest_mock import mocker

# Teste da rota principal
@pytest.fixture
def client():
    # Criação de um cliente de teste para simular requisições HTTP
    with app.test_client() as client:
        yield client

def assert_in_response(response, text):
    """Função auxiliar para comparar strings na resposta de bytes"""
    assert text in response.data.decode('utf-8')

def test_home_page(client):
    # Verifica se a página inicial carrega corretamente com o método GET
    response = client.get('/')
    assert response.status_code == 200
    assert_in_response(response, "Consulta de CEP")  # Verifica se o texto da página está presente

def test_consulta_cep_valido(client, mocker):
    # Simulando uma requisição POST com um CEP válido
    mock_response = {
        "cep": "01001-000",
        "logradouro": "Praça da Sé",
        "bairro": "Sé",
        "localidade": "São Paulo",
        "uf": "SP",
        "ibge": "3550308",
        "gia": "1004",
        "ddd": "11",
        "siafi": "6210"
    }

    # Mock da requisição para a API ViaCEP (não chama a API real)
    mocker.patch('requests.get', return_value=mocker.Mock(status_code=200, json=lambda: mock_response))

    response = client.post('/', data={'cep': '01001-000'})
    assert response.status_code == 200
    assert_in_response(response, "Praça da Sé")  # Verifica se o logradouro retornado está na página

def test_consulta_cep_invalido(client, mocker):
    # Simulando uma requisição POST com um CEP inválido
    mock_response = {"erro": "true"}

    # Mock da requisição para a API ViaCEP (não chama a API real)
    mocker.patch('requests.get', return_value=mocker.Mock(status_code=200, json=lambda: mock_response))

    response = client.post('/', data={'cep': '00000-000'})
    assert response.status_code == 200
    assert_in_response(response, "CEP não encontrado!")  # Verifica se a mensagem de erro aparece

def test_consulta_cep_sem_cep(client):
    # Testa quando não é fornecido um CEP
    response = client.post('/', data={'cep': ''})
    assert response.status_code == 200
    assert_in_response(response, "Por favor, insira um CEP válido.")  # Verifica se a mensagem de erro aparece
