import Resources from './resource';
import {encode} from "../utils/base64";
import Endpoints from "../endpoints/endpoints";

export default {
    getPermissions(authToken) {
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
        return Resources.get(Endpoints.permissions_data).then(response => response.json());
    }
}