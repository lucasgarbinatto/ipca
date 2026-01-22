# BCB IPCA Top5 Long Period Analysis

This project fetches and analyzes **IPCA (Broad Consumer Price Index) Top5 Long Period** market expectations from the **Banco Central do Brasil (BCB)** OLINDA API.

## Files

- **`ipca_top5.py`** - Python script to fetch IPCA Top5 data from BCB API
- **`ipca_top5_analysis.qmd`** - Quarto document with interactive analysis and visualizations

## Requirements

Install the required packages:

```bash
pip install requests pandas plotly
```

For the Quarto document, you also need:

```bash
pip install jupyter
```

And install Quarto from: https://quarto.org/docs/get-started/

## Usage

### Python Script

```bash
python ipca_top5.py
```

This will:
1. Fetch IPCA Monthly Top5 Long Period data
2. Fetch IPCA Annual Top5 Long Period data
3. Fetch IPCA 12-month Top5 Long Period data
4. Save results to CSV files

### Quarto Document

```bash
quarto render ipca_top5_analysis.qmd
```

This will generate an interactive HTML report with:
- Data tables
- Interactive charts (Plotly)
- Statistical summaries
- Exported CSV files

## API Reference

**Base URL:** `https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata`

### Endpoints Used

| Endpoint | Description |
|----------|-------------|
| `ExpectativaMercadoMensaisTop5` | Monthly Top5 expectations |
| `ExpectativasMercadoAnuaisTop5` | Annual Top5 expectations |
| `ExpectativasMercadoInflacao12MesesTop5` | 12-month inflation Top5 expectations |

### Calculation Types

- **L (Longo Prazo):** Long Period
- **M (Médio Prazo):** Medium Period
- **C (Curto Prazo):** Short Period

## Output Files

| File | Description |
|------|-------------|
| `ipca_monthly_top5_long.csv` | Monthly IPCA Top5 Long Period data |
| `ipca_annual_top5_long.csv` | Annual IPCA Top5 Long Period data |
| `ipca_12months_top5_long.csv` | 12-month IPCA Top5 Long Period data |

## Documentation

- [BCB OLINDA API Documentation](https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/documentacao)
- [Banco Central do Brasil - Focus Report](https://www.bcb.gov.br/publicacoes/focus)
