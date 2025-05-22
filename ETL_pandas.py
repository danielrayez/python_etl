import pandas as pd 
import time
import re

inicio = time.time()
# Diccionario para convertir meses en español a números
meses = {"ene": "01", "feb": "02", "mar": "03", "abr": "04", "may": "05", "jun": "06",
         "jul": "07", "ago": "08", "sep": "09", "oct": "10", "nov": "11", "dic": "12"}

ruta = r"C:\Users\danie\OneDrive\Escritorio\Datos\Excel\Practicas Data Analysis\etl_Python\Datos.xlsx"

df = pd.read_excel(ruta,  sheet_name= 'Hoja2 RF04', skiprows= 4, header = 0)

df_cajas = df[['CANAL','GRUPO',  'CODIGO','abr-25', 'may-25', 'jun-25', 'jul-25', 'ago-25', 'sep-25',
            'oct-25', 'nov-25', 'dic-25', 'ene-26', 'feb-26', 'mar-26',]]

#ANULO DINAMIZACIÓN DE FECHAS
df_cajas = df_cajas.melt(id_vars= ['CANAL','GRUPO',  'CODIGO'], var_name= "Fecha", value_name= "Valor")
df_cajas['Fecha'] = df_cajas['Fecha'].str.replace("-", "_", regex= True)

##Precios
df_precios = df[[ 'CANAL','GRUPO',  'CODIGO', 'abr_25-Pr Netos', 'may_25-Pr Netos', 'jun_25-Pr Netos', 'jul_25-Pr Netos',
                 'ago_25-Pr Netos', 'sep_25-Pr Netos', 'oct_25-Pr Netos', 'nov_25-Pr Netos', 'dic_25-Pr Netos',
                  'ene_26-Pr Netos', 'feb_26-Pr Netos', 'mar_26-Pr Netos']]
#ANULO DINAMIZACIÓN DE FECHAS
df_precios = df_precios.melt(id_vars= ['CANAL','GRUPO',  'CODIGO'], var_name= "Fecha", value_name= "Valor")
df_precios['Fecha'] = df_precios['Fecha'].str.replace("-Pr Netos", "", regex= True)

##FAP
df_fap = df[[ 'CANAL','GRUPO',  'CODIGO', 'Abr_25 FAP','May_25 FAP', 'Jun_25 FAP', 'Jul_25 FAP', 'Ago_25 FAP', 'Sep_25 FAP',
            'Oct_25 FAP', 'Nov_25 FAP', 'Dic_25 FAP', 'Ene_26 FAP', 'Feb_26 FAP', 'Mar_26 FAP',]]

#ANULO DINAMIZACIÓN DE FECHAS
df_fap = df_fap.melt(id_vars= ['CANAL','GRUPO',  'CODIGO'], var_name= "Fecha", value_name= "Valor")
df_fap['Fecha'] = df_fap['Fecha'].str.replace(" FAP", "", regex= True).str.lower()


df_ptp = df[[ 'CANAL','GRUPO',  'CODIGO',  'Abr_25 PTP $$', 'May_25 PTP $$', 'Jun_25 PTP $$', 'Jul_25 PTP $$', 'Ago_25 PTP $$',
            'Sep_25 PTP $$', 'Oct_25 PTP $$', 'Nov_25 PTP $$', 'Dic_25 PTP $$', 'Ene_26 PTP $$', 'Feb_26 PTP $$', 'Mar_26 PTP $$']]

#ANULO DINAMIZACIÓN DE FECHAS
df_ptp = df_ptp.melt(id_vars= ['CANAL','GRUPO',  'CODIGO'], var_name= "Fecha", value_name= "Valor")
df_ptp["Fecha"] = df_ptp["Fecha"].apply(lambda x: re.sub(r"\s*PTP\s*\$\$", "", x)).str.lower()

#Funcion para transformación generica de todos los df
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

df_cajas = transformar_df(df_cajas)
df_precios = transformar_df(df_precios)
df_fap = transformar_df(df_fap)
df_ptp = transformar_df(df_ptp)

df_final = (
    df_cajas
    .merge(df_precios[['LLave', 'Valor']], how='left', on='LLave', suffixes=('', '_Precio'))
    .merge(df_fap[['LLave', 'Valor']], how='left', on='LLave', suffixes=('', '_FAP'))
    .merge(df_ptp[['LLave', 'Valor']], how='left', on='LLave', suffixes=('', '_PTP'))
)
df_final.rename(columns={'Valor':'Cajas'}, inplace= True)

df_final['Fact_Operativa'] = (df_final['Cajas'] * df_final['Valor_Precio'] ) /1000

print(df_final.head(5))

fin = time.time()
print(f"tiempo de lectura: {fin-inicio:.2f} segundos ")