import json
from collections import defaultdict

# --- Carregar dados ---
with open("expectativas_filtradas.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

# --- Pegar apenas a data de pesquisa mais recente ---
data_mais_recente = max(d["Data"] for d in dados)
dados_filtrados = [d for d in dados if d["Data"] == data_mais_recente]

print(f"=" * 60)
print(f"ANÁLISE DAS EXPECTATIVAS DE IPCA - TOP 5 BCB")
print(f"Data da pesquisa: {data_mais_recente}")
print(f"=" * 60)

# --- Organizar por mês de referência ---
expectativas = {}
for d in dados_filtrados:
    ref = d["DataReferencia"]  # formato: "MM/YYYY"
    expectativas[ref] = {
        "mediana": d["Mediana"],
        "media": d["Media"],
        "minimo": d["Minimo"],
        "maximo": d["Maximo"],
        "desvio": d["DesvioPadrao"]
    }

# --- Função para calcular inflação acumulada (composta) ---
def calcular_inflacao_acumulada(taxas_mensais):
    """
    Calcula inflação acumulada usando fórmula composta:
    (1 + r1/100) * (1 + r2/100) * ... * (1 + rn/100) - 1
    Retorna em percentual
    """
    acumulado = 1.0
    for taxa in taxas_mensais:
        acumulado *= (1 + taxa / 100)
    return (acumulado - 1) * 100

# --- Definir meses por ano ---
meses_2026 = [f"{m:02d}/2026" for m in range(1, 13)]
meses_2027 = [f"{m:02d}/2027" for m in range(1, 13)]

# --- Função para exibir análise de um ano ---
def analisar_ano(ano, meses):
    print(f"\n{'=' * 60}")
    print(f"EXPECTATIVAS MENSAIS DE IPCA - {ano}")
    print(f"{'=' * 60}")
    print(f"{'Mês':<12} {'Mediana':>10} {'Mínimo':>10} {'Máximo':>10} {'Desvio':>10}")
    print("-" * 60)
    
    taxas_mensais = []
    trimestres = defaultdict(list)
    
    for i, mes in enumerate(meses, 1):
        if mes in expectativas:
            exp = expectativas[mes]
            taxas_mensais.append(exp["mediana"])
            
            # Determinar trimestre (1-3: Q1, 4-6: Q2, 7-9: Q3, 10-12: Q4)
            trimestre = (i - 1) // 3 + 1
            trimestres[trimestre].append(exp["mediana"])
            
            print(f"{mes:<12} {exp['mediana']:>10.4f}% {exp['minimo']:>10.4f}% {exp['maximo']:>10.4f}% {exp['desvio']:>10.4f}")
        else:
            print(f"{mes:<12} {'N/D':>10} {'N/D':>10} {'N/D':>10} {'N/D':>10}")
    
    # --- Inflação acumulada 12 meses ---
    if taxas_mensais:
        inflacao_12m = calcular_inflacao_acumulada(taxas_mensais)
        soma_simples = sum(taxas_mensais)
        
        print("-" * 60)
        print(f"\n📊 INFLAÇÃO ACUMULADA {ano} (12 meses)")
        print(f"   Acumulada (composta): {inflacao_12m:.2f}%")
        print(f"   Soma simples:         {soma_simples:.2f}%")
        
        # Identificar meses críticos
        if taxas_mensais:
            max_taxa = max(taxas_mensais)
            min_taxa = min(taxas_mensais)
            mes_max = meses[taxas_mensais.index(max_taxa)]
            mes_min = meses[taxas_mensais.index(min_taxa)]
            media_mensal = sum(taxas_mensais) / len(taxas_mensais)
            
            print(f"\n📈 INSIGHTS {ano}:")
            print(f"   Maior expectativa:  {max_taxa:.4f}% em {mes_max}")
            print(f"   Menor expectativa:  {min_taxa:.4f}% em {mes_min}")
            print(f"   Média mensal:       {media_mensal:.4f}%")
    
    # --- Inflação por trimestre ---
    print(f"\n📅 INFLAÇÃO POR TRIMESTRE {ano}")
    print(f"{'Trimestre':<15} {'Meses':<20} {'Acumulado':>12}")
    print("-" * 50)
    
    nomes_trimestres = {
        1: "Q1 (Jan-Mar)",
        2: "Q2 (Abr-Jun)",
        3: "Q3 (Jul-Set)",
        4: "Q4 (Out-Dez)"
    }
    
    for q in range(1, 5):
        if q in trimestres and trimestres[q]:
            acum_tri = calcular_inflacao_acumulada(trimestres[q])
            n_meses = len(trimestres[q])
            print(f"{nomes_trimestres[q]:<15} {n_meses} meses{'':<13} {acum_tri:>10.2f}%")
        else:
            print(f"{nomes_trimestres[q]:<15} {'N/D':<20} {'N/D':>12}")
    
    return taxas_mensais, trimestres

# --- Executar análise para 2026 e 2027 ---
taxas_2026, tri_2026 = analisar_ano(2026, meses_2026)
taxas_2027, tri_2027 = analisar_ano(2027, meses_2027)

# --- Comparativo entre anos ---
print(f"\n{'=' * 60}")
print("📊 COMPARATIVO 2026 vs 2027")
print(f"{'=' * 60}")

if taxas_2026 and taxas_2027:
    inf_2026 = calcular_inflacao_acumulada(taxas_2026)
    inf_2027 = calcular_inflacao_acumulada(taxas_2027)
    diferenca = inf_2027 - inf_2026
    
    print(f"   Inflação acumulada 2026: {inf_2026:.2f}%")
    print(f"   Inflação acumulada 2027: {inf_2027:.2f}%")
    print(f"   Diferença (2027-2026):   {diferenca:+.2f}%")
    
    if diferenca > 0:
        print(f"\n   ⚠️  Expectativa de AUMENTO da inflação em 2027")
    elif diferenca < 0:
        print(f"\n   ✅ Expectativa de REDUÇÃO da inflação em 2027")
    else:
        print(f"\n   ➡️  Expectativa de inflação ESTÁVEL")

# --- Meta de inflação ---
print(f"\n{'=' * 60}")
print("🎯 COMPARAÇÃO COM META DE INFLAÇÃO")
print(f"{'=' * 60}")
META_INFLACAO = 3.0  # Meta do BCB
TETO_META = 4.5      # Teto (meta + 1.5pp)

if taxas_2026:
    inf_2026 = calcular_inflacao_acumulada(taxas_2026)
    desvio_meta = inf_2026 - META_INFLACAO
    
    print(f"   Meta de inflação:     {META_INFLACAO:.1f}%")
    print(f"   Teto da meta:         {TETO_META:.1f}%")
    print(f"   Expectativa 2026:     {inf_2026:.2f}%")
    print(f"   Desvio da meta:       {desvio_meta:+.2f}pp")
    
    if inf_2026 <= META_INFLACAO:
        print(f"\n   ✅ Expectativa DENTRO da meta")
    elif inf_2026 <= TETO_META:
        print(f"\n   ⚠️  Expectativa ACIMA da meta, mas dentro do teto")
    else:
        print(f"\n   🚨 Expectativa ACIMA do teto da meta!")

print(f"\n{'=' * 60}")
print("Análise concluída!")
print(f"{'=' * 60}")
