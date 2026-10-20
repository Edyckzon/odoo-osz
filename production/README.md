# VPS: preparacion por etapas

Estos archivos preparan el entorno; NO habilitan CD ni migran la base local.
No publicar Caddy hasta inicializar osz_erp, configurar un administrador con
clave nueva y verificar backups/restauracion. Sin datos demo. El dominio
previsto es odoo.grupoaym.com. No se ha modificado el VPS desde este repositorio.

## 1. Preparar, sin iniciar servicios

Clonar el repositorio en /opt/osz-erp como root. Desde esa carpeta:

```bash
sudo python3 production/prepare.py
sudo docker compose --env-file production/.env -f production/compose.yaml config --quiet
sudo docker compose --env-file production/.env -f production/compose.yaml build odoo
```

Las claves quedan en archivos ignorados por Git. prepare.py no sobrescribe
archivos. La configuracion montada pertenece al UID 100/GID 101 de la imagen
fijada; el directorio padre solo es accesible por root en el host.
PostgreSQL usa un rol Odoo sin privilegios de superusuario ni CREATEDB.
La base se crea en el primer arranque mediante init-db.sh.

## 2. Arranque interno (siguiente etapa)

Crear osz_erp_proxy, iniciar db e inicializar Odoo en osz_erp mediante un
contenedor temporal --stop-after-init. Configurar credenciales de administrador
antes de arrancar el servicio publico. Nunca usar la clave predeterminada.
La imagen propia incluye los addons; no incluye secretos, bases ni el clon Odoo.
Una vez inicializado, arrancar odoo y comprobar salud/login/modulo instalado.

## 3. Integrar Caddy y DNS

Respaldar /opt/grupoaym/compose.yaml y el directorio caddy. El override agrega
una red sin retirar default. Incorporarlo de forma persistente en el Compose
del proyecto VPN, conservando cualquier override que exista. No depender de
docker network connect manual. Recrear solo caddy puede interrumpir brevemente
las conexiones HTTP de la VPN. Headscale no necesita recrearse.

odoo.caddy es la propuesta para /opt/grupoaym/caddy/sites/odoo.caddy.
Validar Caddy antes de recargar. Crear registro A odoo hacia la IP del VPS,
inicialmente solo DNS. Verificar HTTPS y websocket. No publicar 8069/8072/5432.

## 4. Pendiente antes de datos reales y CD

- Backup consistente de PostgreSQL y filestore, copia externa y restauracion probada.
- Revision de firewall, alertas de espacio/salud y retencion de respaldos.
- Imagen GHCR por digest, credenciales restringidas y despliegues serializados.
- Procedimiento de migraciones: volver a una imagen NO revierte la base.
- Prueba de carga para ajustar limites. Este VPS no ofrece alta disponibilidad.

No ejecutar down --volumes sobre datos persistentes. No usar el Compose local
para produccion. La imagen osz-erp:<commit> es una etiqueta local inicial;
el pipeline de publicacion GHCR todavia no esta implementado.

## Migracion a Liquid Glass + OSZ ERP

Tras comprobar CI: `sudo git pull --ff-only && sudo bash production/install-theme.sh`
desde `/opt/osz-erp`. La migracion reconstruye la imagen y hace un respaldo
consistente (base + filestore + secretos) antes de cambiar los modulos.
Retira el antiguo launcher si esta instalado usando la imagen anterior, luego
instala Liquid Glass y actualiza la identidad OSZ. No modifica Caddy, DNS ni VPN.
Existe una breve ventana sin servicio mientras se migran los modulos.
Ante un error despues de detener Odoo, se conserva el respaldo y se detiene el
despliegue para diagnosticar; no se intenta revertir solo la imagen.

Verificar luego: HTTPS/login con logo OSZ, acceso del administrador, menu y
navegacion a ventas/facturacion, formularios y acceso movil. La comprobacion
de salud del contenedor no reemplaza esta revision funcional.
