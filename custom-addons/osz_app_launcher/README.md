# OSZ: menu de aplicaciones

Modulo independiente para Odoo Community 19. Reemplaza el selector desplegable
de escritorio por una cuadricula a pantalla completa. En movil agrega el acceso
a la cuadricula y conserva el menu de secciones. No cambia el inicio de sesion
ni fuerza una pantalla al abrir enlaces directos.

Solo consume `menu.getApps()` y navega con `menu.selectMenu()`: utiliza los menus
que Odoo entrega al usuario, sin nuevas ACL ni permisos. No instala otras apps.
Iconos originales, busqueda sin distinguir tildes, Enter para abrir el primer
resultado, Escape para cerrar, Tab para navegar. Los enlaces conservan Ctrl/cmd
para abrir en otra pestana. El tema claro/oscuro se guarda en el navegador y
solo afecta al lanzador, no al resto de Odoo.

## Instalar en el VPS existente

Revisar que CI pase, actualizar el clon y ejecutar desde /opt/osz-erp:

```bash
sudo git pull --ff-only
sudo bash production/install-launcher.sh
```

El script construye antes de detener Odoo, bloquea despliegues concurrentes,
respalda BD y filestore con Odoo detenido, instala el modulo y espera la salud
del servicio. Caddy y la VPN no se modifican. Hay una interrupcion breve del ERP.
La copia esta en el mismo VPS; siguen pendientes copia externa y restauracion
ensayada. Si falla, conservar el error y los respaldos y revisar antes de seguir.
No restaurar solo la imagen si el esquema de la base ha cambiado.

Se puede desinstalar solo este modulo para recuperar el selector original.
