import requests
import smtplib
from email.message import EmailMessage
import os

def bot_dolar_oficial():
    # 1. BUSCAR EL PRECIO DEL DÓLAR OFICIAL
    try:
        url = "https://dolarapi.com/v1/dolares/oficial"
        datos = requests.get(url).json()
        precio_hoy = datos['venta']
        print(f"Dólar oficial hoy: ${precio_hoy}")
    except Exception as e:
        print(f"Error al conectar con la API: {e}")
        return

    # 2. LÓGICA DE MEMORIA (En GitHub el archivo está en la misma carpeta)
    archivo_memoria = "ultimo_precio.txt"
    
    # Si el archivo no existe, lo creamos y avisamos
    if not os.path.exists(archivo_memoria):
        with open(archivo_memoria, "w") as f:
            f.write(str(precio_hoy))
        print("Primer registro guardado. Mañana podré comparar.")
        return

    # Leemos el precio guardado anteriormente
    with open(archivo_memoria, "r") as f:
        contenido = f.read().strip()
        precio_ayer = float(contenido)

    # 3. CONFIGURACIÓN (RELLENÁ CON TUS DATOS) ------------------
    tu_correo = "erikaaleuy8@gmail.com" 
    tu_clave_16 = "rllwdsuplzjdnttg" 
    # --------------------------------------------------------------

    # 4. COMPARAR Y ENVIAR SI BAJÓ
    print(f"Comparando: Hoy ${precio_hoy} vs Ayer ${precio_ayer}")
    
    if precio_hoy < precio_ayer:
        msg = EmailMessage()
        msg['Subject'] = f"📉 ¡BAJÓ EL DÓLAR! Oficial a ${precio_hoy}"
        msg['From'] = tu_correo
        msg['To'] = tu_correo
        
        cuerpo = f"""
        ¡Hola! El dólar oficial bajó.
        Precio anterior: ${precio_ayer}
        Precio nuevo: ${precio_hoy}
        """
        msg.set_content(cuerpo)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(tu_correo, tu_clave_16.replace(" ", ""))
                smtp.send_message(msg)
            print("✅ Mail de alerta enviado.")
        except Exception as e:
            print(f"Error al enviar el mail: {e}")
    else:
        print("El precio no bajó. No se envía mail.")

    # 5. ACTUALIZAR LA MEMORIA PARA LA PRÓXIMA VEZ
    with open(archivo_memoria, "w") as f:
        f.write(str(precio_hoy))

if __name__ == "__main__":
    bot_dolar_oficial()
