# OSZ ERP

Personalizaciones propias sobre Odoo Community 19. Entorno local con PostgreSQL 16.
El codigo de Odoo pertenece a sus autores; este repositorio no incluye Enterprise.
El modulo `osz_branding` declara licencia LGPL-3 e integra Liquid Glass con
el logo y titulo OSZ ERP. La empresa y sus documentos conservan su identidad.

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

CD al VPS todavia no esta habilitado. `compose.yaml` es exclusivamente local;
`production/compose.yaml` usa una imagen OSZ, red dedicada con Caddy,
PostgreSQL interno y secretos en el servidor. Ver `production/README.md`.
Volver a una imagen anterior no revierte migraciones de base de datos.

Destino previsto: `odoo.grupoaym.com`. La integracion NubeFact/SUNAT aun no esta
implementada. No se incluyen bases ni datos de empresas.

## Tema y marca del producto

Liquid Glass 19 de Cybrosys esta incluido, fijado a un commit y sin editar.
Ver `third-party/README.md` y `scripts/verify-vendor.py`. El menu propio
`osz_app_launcher` fue retirado; MuK no forma parte de esta instalacion.
Los cambios OSZ son logo de acceso/menu, favicon y titulo; no alteran el nombre,
RUC o logo de `res.company`. Se conserva la atribucion a Odoo en el acceso.
El pie del acceso agrega "Personalizado por OneSecureZone", enlazado al sitio
del autor de las personalizaciones. Acceso, registro y recuperacion usan
espanol de Peru (`es_PE`) con las traducciones oficiales, incluso si el
navegador solicita ingles. No se modifica el idioma guardado de los usuarios.

Para actualizar el VPS desde la version anterior, despues de CI exitoso:

```bash
cd /opt/osz-erp
sudo git pull --ff-only && sudo bash production/install-theme.sh
```

El script respalda base y filestore con Odoo detenido, desinstala el launcher
usando la imagen anterior, instala Liquid Glass y actualiza `osz_branding`.
La copia local no sustituye un respaldo externo. Una recuperacion requiere
restaurar base, filestore y configuracion del mismo respaldo, ademas de la
imagen anterior. No basta con volver al commit anterior.
