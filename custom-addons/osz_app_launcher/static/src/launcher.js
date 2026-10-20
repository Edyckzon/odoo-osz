/** @odoo-module **/
import { Component, useState } from '@odoo/owl';
import { Dialog } from '@web/core/dialog/dialog';
import { browser } from '@web/core/browser/browser';
import { useAutofocus, useBus, useService } from '@web/core/utils/hooks';
import { patch } from '@web/core/utils/patch';
import { NavBar } from '@web/webclient/navbar/navbar';

const THEME_KEY = 'osz.appLauncher.theme';
const normalize = (value) => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase();

export class OszAppLauncher extends Component {
    static template = 'osz_app_launcher.Launcher';
    static components = { Dialog };
    static props = { close: Function };

    setup() {
        this.menu = useService('menu');
        let theme;
        try {
            theme = browser.localStorage.getItem(THEME_KEY);
        } catch { /* Storage may be disabled by the browser. */ }
        this.state = useState({
            query: '',
            busy: false,
            theme: ['light', 'dark'].includes(theme) ? theme :
                (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'),
        });
        useAutofocus();
        useBus(this.env.bus, 'MENUS:APP-CHANGED', () => this.render());
    }

    get apps() {
        const query = normalize(this.state.query.trim());
        // Odoo supplies only menus available to the current user/company context.
        return this.menu.getApps().filter((app) => normalize(app.name).includes(query));
    }

    toggleTheme() {
        this.state.theme = this.state.theme === 'light' ? 'dark' : 'light';
        try {
            browser.localStorage.setItem(THEME_KEY, this.state.theme);
        } catch { /* Keep the selected theme for this opening. */ }
    }

    href(app) {
        return `/odoo/${app.actionPath || 'action-' + app.actionID}`;
    }

    async openApp(app, event) {
        if (event && (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey)) {
            return;
        }
        event?.preventDefault();
        if (this.state.busy) {
            return;
        }
        this.state.busy = true;
        try {
            await this.menu.selectMenu(app);
            this.props.close();
        } finally {
            this.state.busy = false;
        }
    }

    onSearchKeydown(event) {
        if (event.key === 'Enter' && !event.isComposing && this.apps.length) {
            return this.openApp(this.apps[0], event);
        }
    }
}

patch(NavBar.prototype, {
    setup() {
        super.setup(...arguments);
        this.oszDialog = useService('dialog');
    },
    openOszLauncher() {
        this._closeAppMenuSidebar();
        this.oszDialog.add(OszAppLauncher, {});
    },
});
