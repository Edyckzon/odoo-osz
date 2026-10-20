FROM odoo:19.0@sha256:d7b19ac51bf8eddba38f53395451681b4b54b68daf905b698b3b9133f954f51f
COPY --chown=odoo:odoo custom-addons/ /mnt/extra-addons/
