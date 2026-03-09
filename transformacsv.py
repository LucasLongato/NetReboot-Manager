import pandas as pd

# Lê o arquivo CSV
df = pd.read_csv("computers.csv")

# Mostra como tabela
print(df)

# Se quiser abrir em formato de planilha no Excel depois:
df.to_excel("saida.xlsx", index=False)
