# Third-party code and product identity

The active theme is MuK Backend Theme 19.0.1.4.9 (LGPL-3) from MuK IT:
https://github.com/muk-it/odoo-modules/tree/2f8e34215ca0f3bab77305917d9bc5e39b44bbca

The seven unmodified modules and their versions/hashes are recorded in
`muk.lock.json`. Upstream authorship, licenses and documentation are preserved.
`MuK-LICENSE` is the upstream repository license. Use the 19.0 release with
Odoo 19; a theme for 20.0 is not a substitute.

The following legacy theme is retained only for safe uninstallation from
existing databases. Do not activate it alongside MuK.

`custom-addons/theme_liquid_glass` is an unmodified copy from Cybrosys:
https://github.com/CybroOdoo/CybroAddons/tree/6cd3b28594ef6abebdfbe7c9092f7ea3fed01688/theme_liquid_glass

Upstream declares LGPL-3, version 19.0.1.0.0. Copyright, authorship and
documentation are preserved. The lock records the source revision and file
hashes; `python3 scripts/verify-vendor.py` verifies them. Upgrade deliberately,
test against the pinned Odoo image, and refresh the lock only after review.

OSZ ERP is the product identity. It does not replace Odoo, MuK IT or Cybrosys authorship.
The login retains its Odoo attribution. Company names, tax IDs, report logos
and document layouts are independent and are not modified by this module.

The OSZ symbol and favicon originate from the owner's site:
https://onesecurezone.com/assets/brand/logo-inverse.svg
https://onesecurezone.com/assets/brand/favicon.svg
The OSZ ERP wordmark adapts that symbol for this product at the owner's request.
Assets: `custom-addons/osz_branding/static/img/` (normal, inverse, favicon).
