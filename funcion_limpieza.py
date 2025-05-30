import pandas as pd

#Funcion para transformación generica de todos los df
# Diccionario para convertir meses en español a números
meses = {"ene": "01", "feb": "02", "mar": "03", "abr": "04", "may": "05", "jun": "06",
         "jul": "07", "ago": "08", "sep": "09", "oct": "10", "nov": "11", "dic": "12"}


def transformar_df(df):

  df["Fecha"] = df["Fecha"].astype(str)  # Asegura que sea string
  #Para cambiar Fecha al formato correcto, necesito transformar el string. Separo la columna
  
  df[['Mes', 'Año']] = df['Fecha'].str.split("_", expand= True)

  #Cambio el nombre del mes por su número
  df['Mes'] = df["Mes"].map(meses)

  #Agrego primer dia del mes y corrijo año
  df['dia'] = '01'
  df['Año'] = "20" + df['Año']

  #Combino dia,mes y año
  df= df[['CANAL','GRUPO', 'CODIGO', 'Valor','Mes','Año','dia']]
  df['Fecha'] = pd.to_datetime( df['Mes']+ "-"+ df['dia'] + "-" + df['Año'])
  df.drop(columns=['Mes','Año','dia'], inplace=True)

  #LLave para combinar dataframes
  df['LLave'] = df['CANAL'] + df['GRUPO'] + df['CODIGO'].astype(str) + df["Fecha"].astype(str)

  return df