import pandas as pd

primes = pd.read_excel("/Users/othmanbensouda/PycharmProjects/Agecap Automatic Forms/files/sehassur_devis.xlsx")

for column in primes.columns[1:]:
    print(column)

