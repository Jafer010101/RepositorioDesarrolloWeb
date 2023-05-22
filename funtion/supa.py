import os
from dotenv import load_dotenv
import supabase

# carga las variables de entorno desde el archivo .env
load_dotenv()

# obtiene las variables de entorno
SUPABASE_URL = "https://ymhtktsffxmaajexzney.supabase.co/rest/v1/Productos?select=*"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InltaHRrdHNmZnhtYWFqZXh6bmV5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY4NDA0NDcyNCwiZXhwIjoxOTk5NjIwNzI0fQ.aw9AKo_rs39WTNGjorSexD79k-Izt5cmUdDCnBcVXfM"

# crea una instancia de cliente Supabase
client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

# consulta los productos de la tabla Productos
response = client.from_('Productos').select('*').execute()

# imprime los datos obtenidos




def datos(url, clave):
    SUPABASE_URL = url
    SUPABASE_KEY = clave
    client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)
    response = client.from_('Productos').select('*').execute()
    lista= str(response)
    texto_formateado= lista
    inicio_datos = texto_formateado.index("[{")
    fin_datos = texto_formateado.index("}]")
    datos_texto = texto_formateado[inicio_datos:fin_datos+2]
    datos_lista = eval(datos_texto)
    return(datos_lista)


