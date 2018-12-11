import Resources from './resource';
import Endpoints from '../endpoints/endpoints'
import {encode, decode} from '../utils/base64';

export default {
    id:-1,
    username:'',
    fullname:'',
    email:'',
    year:'',
    token:'',
    isLogued() {
        return this.token !== '';
    },
    logOut() {
        this.id = -1;
        this.username = '';
        this.fullname = '';
        this.email = '';
        this.year = '';
        this.token = '';
    },
    updateToken(token) {
        this.token = token;
    },
    updateId(id) {
        this.token = id;
    },
    getAuthJson(username, password) {
        Resources.clearHeaders();
        Resources.setHeaders(
            [{
                key: 'Authorization',
                value: 'Basic ' + encode(username + ':' + password)
            },
            {
                key: 'Content-Type',
                value: 'application/json'
            },
            {
                key: 'Accept',
                value: 'application/json'
            }
        ]);
        return Resources.get(Endpoints.token_endpoint).then(response => response.json(), response => console.log('Error retriving json'));
    },
    authenticateUser(username, password) {
        return this.getAuthJson(username, password)
            .then(json => {
                if (json.token != null && json.id != null) {
                    this.updateToken(json.token);
                    this.updateId(json.id);
                    return true;
                }
                console.log(json.error + ':' + json.message);
                return false;
            });
    }
}