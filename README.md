# OSZ ERP

Personalizaciones propias sobre Odoo Community 19. Entorno local con PostgreSQL 16.
El codigo de Odoo pertenece a sus autores; este repositorio no incluye Enterprise.
El modulo `osz_branding` declara licencia LGPL-3 y cambia el titulo del navegador.

## Iniciar un clon nuevo

Requisitos: Docker Engine/Desktop con Compose y Python 3 para generar configuracion.

```bash
python3 scripts/init-local.py
docker compose up -d
```

En Windows puede usarse `python` o `py -3`. Abrir http://localhost:8069 y crear
una base sin datos demo. La clave maestra generada esta en `config/odoo.conf`.
El script rechaza sobrescribir configuracion existente. No ejecutarlo para
rotar claves de una base ya inicializada.

Los modulos propios estan en `custom-addons`. El clon opcional `odoo/` es solo
referencia y no se publica ni se ejecuta por este Compose. Las imagenes oficiales
estan fijadas por digest. Tras crear la base, instalar `osz_branding` desde Apps.

## Datos y secretos

`.env`, configuracion real, SQL de inicializacion y credenciales locales estan
excluidos de Git. Los datos viven en volumenes Docker. No ejecutar
`docker compose down --volumes` en desarrollo con datos o produccion.
Los respaldos deben incluir PostgreSQL y el filestore correspondiente.

## CI y despliegue

GitHub Actions valida Compose/Python e instala el modulo en una base temporal en
cada push a main y pull request. La eliminacion de volumenes del workflow solo
afecta al entorno efimero de CI. El resultado remoto debe comprobarse en Actions.

CD al VPS todavia no esta habilitado. El Compose actual es exclusivamente local;
no debe publicarse tal cual en Internet. Proximo paso: Compose de produccion,
imagen OSZ inmutable, red dedicada con Caddy, PostgreSQL interno, secretos en el
servidor, backup/restauracion verificados y despliegue serializado por release.
Volver a una imagen anterior no revierte migraciones de base de datos.

Destino previsto: `odoo.grupoaym.com`. La integracion NubeFact/SUNAT aun no esta
implementada. No se incluyen bases ni datos de empresas.
