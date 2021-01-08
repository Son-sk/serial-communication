from os import sep
import pandas as pd

data = pd.read_csv('202118.csv', sep=",", error_bad_lines=False)

print(data)

data.to_csv('202118_to.csv')