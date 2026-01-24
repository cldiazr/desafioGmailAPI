# desafioGmailAPI

Una aplicación desarrollada en Python 3.11+ que interactúa con la API de Gmail para analizar los correos electrónicos en busca de contenido sensible (palabras claves) y adjuntos con extensiones prohibidas.

Este proyecto fue desarrollado como parte de un reto técnico, implementando autenticación OAuth 2.0, análisis de texto/archivos y notificaciones externas vía Webhook.

## Características

    * Autenticación Segura: Conexión vía OAuth 2.0 con Google (scope `readonly`).
    * Análisis de Contenido: Escaneo automático de palabras clave sensibles (`confidencial`, `contraseña`) en el asunto y cuerpo del correo.
    * Detección de adjuntos: Identificación de adjuntos con extensiones prohibidas (`.exe`, `.bat`, `.js`, `.zip`), incluyendo detección de doble extensión.
    * Lista Blanca (Whitelist): Filtrado de correos provenientes de dominios confiables (ej. `@google.com`).
    * Sistema de Alertas:
        * Registro local en archivo `alertas.txt` (evitando duplicados).
        * Notificación en tiempo real vía Webhook.

## Requisitos Previos

    * Python 3.10 o superior.
    * Una cuenta de Google Cloud Platform con la "Gmail API" habilitada.
    * Archivo `credentials.json` descargado de GCP (OAuth 2.0 Client ID).

## Instalación

    1.  Clonar el repositorio:

        git clone https://github.com/cldiazr/desafioGmailAPI.git
        cd desafioGmailAPI

    2.  Crear y activar entorno virtual (recomendado para evitar conflictos con librerias instaladas de forma global):

        python -m venv venv
        # En Windows:
        .\venv\Scripts\activate
        # En Mac/Linux:
        source venv/bin/activate

    3.  Instalar dependencias:

        pip install -r requirements.txt

    4.  Configuración de Credenciales:
        * Coloca tu archivo `credentials.json` en la raíz del proyecto.

## Configuración

    * Webhook
        El sistema está configurado para enviar alertas a un endpoint externo.
        * El archivo `webhookAlert.py` contiene la variable `WEBHOOK_URL`.
        * Para pruebas, se utilizó "Webhook.site".
        Nota: Puedes cambiar esta URL por tu propio endpoint para ver las notificaciones en tu entorno.

    * Whitelist
    Los dominios seguros se configuran en la lista `DOMINIOS_SEGUROS` dentro del archivo `viewMessagesTest.py`.

## Ejecución

Para iniciar el análisis del buzón:

    python viewMessagesTest.py
        # Al ejecutarse por primera vez, se abrirá el navegador para solicitar permisos de lectura de Gmail.
        Una vez autorizado, el script:

            Creará el token de sesión (token.json).
            Leerá los últimos mensajes del Inbox y SPAM.
            Imprimirá en consola las alertas detectadas.
            Generará/Actualizará el archivo alertas.txt.
            Enviará la notificación al Webhook configurado.

## Estructura del Proyecto

    viewMessagesTest.py: Entry point. Realiza la lectura de mensajes y el flujo principal.

    connectApiGmail.py: Maneja la autenticación OAuth y renovación de tokens.

    condicionalesAlerts.py: Lógica del proyecto (búsqueda de palabas claves y validación de adjuntos).

    webhookAlert.py: Módulo para el envío de peticiones HTTP (alertas externas).

    archivoAlert.py: Manejo de persistencia en archivo de texto.


## Webhook
    
    Dashboard para visualizar las peticiones realizadas de prueba en WebHook

    link : https://webhook.site/#!/view/a68dc9de-1c92-4304-834e-86ac27d80368/ebd46bc4-477c-435c-8702-29d5fb0306e6/1

## Whitelist
    
    Los correos provenientes de dominios como google.com o empresa.com son ignorados automáticamente por el analizador.

Hecho por Christian Diaz