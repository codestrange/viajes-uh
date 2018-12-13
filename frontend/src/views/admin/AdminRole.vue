<template>
    <div id="useradmin" v-if="!this.$store.state.loader.showing">
        <b-container fluid>
            <b-row md="6" class="my-2">
                <b-col md="6" class="my-1">
                    <b-form-group horizontal label="Filtrar" class="mb-0">
                        <b-input-group>
                            <b-form-input v-model="filter" placeholder="Buscar" />
                            <b-input-group-append>
                                <b-btn :disabled="!filter" @click="filter = ''">Limpiar</b-btn>
                            </b-input-group-append>
                        </b-input-group>
                    </b-form-group>
                    <b-form-group horizontal label="Ordenar por" class="mb-0">
                        <b-input-group>
                            <b-form-select v-model="sortBy" :options="sortOptions">
                                <option slot="first" :value="null">-- ninguno --</option>
                            </b-form-select>
                            <b-form-select :disabled="!sortBy" v-model="sortDesc" slot="append">
                                <option :value="false">Asc</option>
                                <option :value="true">Desc</option>
                            </b-form-select>
                        </b-input-group>
                    </b-form-group>
                    <b-form-group horizontal label="Mostrar por Página" class="mb-0">
                        <b-form-select :options="pageOptions" v-model="perPage" />
                    </b-form-group>
                </b-col>
            </b-row>

            <b-table show-empty
                     stacked="md"
                     :items="items"
                     :fields="fields"
                     :current-page="currentPage"
                     :per-page="perPage"
                     :filter="filter"
                     :sort-by.sync="sortBy"
                     :sort-desc.sync="sortDesc"
                     :sort-direction="sortDirection"
                     @filtered="onFiltered"
            >
                <template slot="actions" slot-scope="row">
                    <b-button size="sm" @click.stop="editUser(row.item)" class="mr-1">
                        Editar
                    </b-button>
                </template>
                <template slot="row-details" slot-scope="row">
                    <b-card>
                        <ul>
                            <li v-for="(value, key) in row.item" :key="key">{{ key }}: {{ value}}</li>
                        </ul>
                    </b-card>
                </template>
            </b-table>

            <b-row>
                <b-col md="6" class="my-1">
                    <b-pagination :total-rows="totalRows" :per-page="perPage" v-model="currentPage" class="my-0" />
                </b-col>
            </b-row>

        </b-container>
    </div>
</template>

<script>
    export default {
        data () {
            return {
                items: [
                    {id:0, label: 'Fallo'},
                ],
                fields: [
                    { key: 'id', label: 'Id', sortable: true, sortDirection: 'desc', 'class': 'text-center' },
                    { key: 'label', label: 'Etiqueta', sortable: true },
                ],
                currentPage: 1,
                perPage: 5,
                totalRows: 6,
                pageOptions: [ 5, 10, 15 ],
                sortBy: null,
                sortDesc: false,
                sortDirection: 'asc',
                filter: null,
                modalInfo: { title: '', content: '' }
            }
        },
        computed: {
            sortOptions () {
                // Create an options list from our fields
                return this.fields
                    .filter(f => f.sortable)
                    .map(f => { return { text: f.label, value: f.key } })
            }
        },
        methods: {
            editUser (item) {
                alert('Trying to edit user ' + item.id.toString());
            },
            onFiltered (filteredItems) {
                // Trigger pagination to update the number of buttons/pages due to filtering
                this.totalRows = filteredItems.length
                this.currentPage = 1
            },
            loadRoles() {
                this.items = this.$store.state.roles.getRoles();
            }
        },
        mounted() {
            this.loadRoles();
        }
    }
</script>
