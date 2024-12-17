async function getData() {
    const url = 'http://localhost:8000/api/matches/result-table';
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        const json = await response.json();
        console.log(json);
        return json;
    } catch (error) {
        console.error(error.message);
        return null;
    }
}

import {createApp} from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js'

createApp({
    data() {
        getData().then(data => this.result_table = data)
        return {
            result_table: null
        }
    },
    delimiters: ["[[", "]]"],
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },
    methods: {}
}).mount('#section-results')