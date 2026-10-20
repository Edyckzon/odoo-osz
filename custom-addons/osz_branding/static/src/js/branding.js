/** @odoo-module **/
import { registry } from '@web/core/registry';
registry.category('services').add('osz_branding', {
    dependencies: ['title'],
    start(env, { title }) {
        title.setParts({ app: 'OSZ ERP' });
    },
});
