export default {
    getToken(vue, url, params) {
        let r;
        vue.$http.get(url).then(response => {
            return response.json();
        }, response => {
                console.log(response);
        }).then(json => {
            r = json;
            console.log(json);
        });
        if(r.token) {
            return r.token;
        }
        return '';
    },
    setHeaders(instance, headers) {
        console.log('vue->');
        console.log(instance);
        console.log('done vue');
        instance.interceptors.push((request, prox) => {
            headers.forEach(header => {
                console.log(header.key,header.value);
                request.headers.set(header.key, header.value);
            });
            prox();
        });
    }
}