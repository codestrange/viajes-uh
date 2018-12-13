export default {
    showing: false,
    type: '',
    note: '',
    showNotification(text) {
        this.type = 'primary';
        this.note = text;
        this.showing = true;
    },
    showError(text) {
        this.type = 'danger';
        this.note = text;
        this.showing = true;
    },
    hideAlerts() {
        this.showing = false;
        this.type = '';
        this.note = '';
    },
}