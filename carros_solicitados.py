from main import price_variation
from main import get_price_history


# Usando o Fiat Uno como exemplo
fiat_var = price_variation("cars", "001054-5", "1996-1", "1997-1")
fiat_hist = get_price_history("cars", "001054-5")

# A BMW M2 Competition
bmw_var = price_variation("cars", "009234-7", "2020-1", "2021-1")
bmw_hist = price_variation("cars", "009234-7")

# Audi A3
audi_var = price_variation("cars", "008032-2", "2001-1", "2002-1")
audi_hist = get_price_history("cars", "009234-7")
