import requests
import json
import urllib.parse # Para codificar a URL corretamente

# --- CONFIGURAÇÃO DE DATAS ---
data_inicio_pesquisa = "2026-01-01"  # Data da coleta (início)
data_fim_pesquisa    = "2026-01-22"  # Data da coleta (fim)
# -----------------------------

url_base = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativasMercadoTop5Mensais"

# Construção do Filtro OData
# Usamos 'ge' (greater or equal) e 'le' (less or equal) para o range de datas
filtro = (
    f"Indicador eq 'IPCA' and "
    f"tipoCalculo eq 'L' and "
    f"Data ge '{data_inicio_pesquisa}' and "
    f"Data le '{data_fim_pesquisa}'"
)

# Codificar os filtros para URL (transforma espaços em %20, etc)
filtro_codificado = urllib.parse.quote(filtro)

# Montagem final da URL
full_url = f"{url_base}?$filter={filtro_codificado}&$format=json&$orderby=Data desc"

try:
    print(f"Consultando período: {data_inicio_pesquisa} a {data_fim_pesquisa}...")
    response = requests.get(full_url)
    response.raise_for_status()
    
    data = response.json()['value']
    
    # Salvar
    with open("expectativas_filtradas.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"Sucesso! {len(data)} registros encontrados e salvos.")

except Exception as e:
    print(f"Erro: {e}")
