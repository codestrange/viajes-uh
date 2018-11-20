import Resources from './resource';
import Endpoints from '../endpoints/endpoints'
import {encode, decode} from '../utils/base64';

export default {
    getToken(username, password) {
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
    }
}