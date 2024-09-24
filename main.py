from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# Base URL da API Fipe
BASE_URL = "https://fipe.parallelum.com.br/api/v2"


# Função auxiliar para fazer requests
def make_request(endpoint: str):
    response = requests.get(f"{BASE_URL}{endpoint}")
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Erro ao buscar dados da API Fipe")


# Rota para variação de preço de algum modelo específico de carro entre dois anos
@app.get("/variacao_preco/{vehicle_type}/{fipe_code}/{year1}/{year2}")
def price_variation(vehicle_type: str, fipe_code: str, year1: str, year2: str):
    # Obter o preço do primeiro ano
    year1_data = make_request(f"/{vehicle_type}/{fipe_code}/years/{year1}")

    # Obter o preço do segundo ano
    year2_data = make_request(f"/{vehicle_type}/{fipe_code}/years/{year2}")

    # Convertendo preços para float
    price1 = float(year1_data["price"].replace("R$ ", "").replace(".", "").replace(",", "."))
    price2 = float(year2_data["price"].replace("R$ ", "").replace(".", "").replace(",", "."))

    # Calculando a variação
    variacao_preco = price2 - price1

    # Retornando o resultado
    return {
        "fipe_code": fipe_code,
        "year1": year1,
        "price1": year1_data["price"],
        "year2": year2,
        "price2": year2_data["price"],
        "variação_preço": f"R$ {variacao_preco:.2f}"
    }


@app.get("/price-history/{vehicle_type}/{fipe_code}")
def get_price_history(vehicle_type: str, fipe_code: str):
    # Obter os anos disponíveis para o veículo
    years = make_request(f"/{vehicle_type}/{fipe_code}/years")
    if not years:
        raise HTTPException(status_code=404, detail="Anos não encontrados para o veículo")

    history = []

    # Obter os preços para cada ano disponível
    for year in years:
        year_id = year["code"]
        year_data = make_request(f"/{vehicle_type}/{fipe_code}/years/{year_id}")
        if "price" in year_data:
            history.append({
                "year": year["name"],
                "price": year_data["price"]
            })

    # Retornar o histórico de preços
    return {
        "vehicle_type": vehicle_type,
        "fipe_code": fipe_code,
        "price_history": history
    }


@app.get("/price-history/{vehicle_type}/{fipe_code}")
def get_price_history(vehicle_type: str, fipe_code: str):
    # Obter os anos disponíveis para o veículo
    years = make_request(f"/{vehicle_type}/{fipe_code}/years")

    history = []

    # Obter os preços para cada ano disponível
    for year in years:
        year_id = year["code"]
        year_data = make_request(f"/{vehicle_type}/{fipe_code}/years/{year_id}")
        history.append({
            "year": year["name"],
            "price": year_data["price"]
        })

    # Retornar o histórico de preços
    return {
        "vehicle_type": vehicle_type,
        "fipe_code": fipe_code,
        "price_history": history
    }
