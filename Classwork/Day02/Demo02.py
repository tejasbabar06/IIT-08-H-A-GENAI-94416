import pandasql as ps
import pandas as pd
filepath = "emp_hdr.csv"
df = pd.read_csv(filepath)
print("Data Frame column types : ")
print(df.dtypes)
print("\n Emp Data : ")
print(df)

query = "SELECT job, SUM(sal) total FROM data GROUP BY job"
result = ps.sqldf(query, {"data" : df})
print("\nQuery Results : ")
print(result)