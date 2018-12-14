import Resources from './resource';
import Endpoints from '../endpoints/endpoints';
import {encode} from "../utils/base64";

export default {
    getRoles(authToken) {
        Resources.clearHeaders();
        Resources.setHeaders(
            [{
                key: 'Authorization',
                value: 'Basic ' + encode(authToken + ':')
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
        return Resources.get(Endpoints.roles_data).then(response => response.json());
    }
}