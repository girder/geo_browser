<template>
  <v-container>
    <v-layout row>
      <v-flex
        xs3
        class="ma-1"
      >
        <v-layout column>
          <h1>Collection Search Builder</h1>
          <v-card>
            <h1>Search Filters</h1>
            <v-flex
              v-for="(param, i) in searchParams"
              :key="i"
            >
              <v-card class="my-1">
                <v-layout column>
                  <v-flex shrink>
                    <v-layout
                      class="mx-2"
                      align-center
                      row
                    >
                      <v-radio-group
                        v-model="param.type"
                        row
                      >
                        <v-radio
                          v-for="(type, j) in paramTypes"
                          :key="j"
                          :label="type.label"
                          :value="type.value"
                        />
                      </v-radio-group>
                      <v-flex>
                        <v-btn
                          color="error"
                          flat
                          icon
                          @click="deleteSearchParam(i)"
                        >
                          <v-icon>mdi-delete</v-icon>
                        </v-btn>
                      </v-flex>
                    </v-layout>
                  </v-flex>
                  <v-flex
                    grow
                    class="ma-2"
                  >
                    <v-card flat>
                      <v-text-field
                        v-model="param.key"
                        label="Key"
                        hide-details
                        solo
                        flat
                      />
                      <v-text-field
                        v-if="param.type !== 'date'"
                        v-model="param.value"
                        label="Value"
                        solo
                        flat
                        :rules="getRules(param)"
                      />
                      <v-flex
                        v-else
                        shrink
                      >
                        <v-select
                          :items="dateComparisonTypes"
                          label="Comparison"
                          prepend-inner-icon="mdi-calculator"
                          hide-details
                          @change="selectDateComparisonType"
                        />
                        <v-menu
                          ref="menu"
                          v-model="param.dateMenu"
                          :close-on-content-click="false"
                          lazy
                          transition="scale-transition"
                          offset-y
                          full-width
                          min-width="290px"
                        >
                          <template v-slot:activator="{ on }">
                            <v-text-field
                              v-model="param.value"
                              label="Date"
                              hide-details
                              readonly
                              prepend-inner-icon="mdi-calendar"
                              v-on="on"
                            />
                          </template>
                          <v-date-picker
                            v-model="param.value"
                            no-title
                            scrollable
                          >
                            <v-spacer />
                            <v-btn
                              flat
                              color="primary"
                              @click="param.dateMenu = false"
                            >
                              OK
                            </v-btn>
                          </v-date-picker>
                        </v-menu>
                      </v-flex>
                    </v-card>
                  </v-flex>
                </v-layout>
              </v-card>
            </v-flex>
            <v-btn
              color="success"
              @click="addSearchParam"
            >
              <v-icon>mdi-plus</v-icon>
              Add Item
            </v-btn>
          </v-card>
        </v-layout>
      </v-flex>
      <v-flex
        xs9
        class="ma-1"
      >
        <v-layout column>
          <v-layout
            row
            shrink
          >
            <v-flex xs11>
              <v-text-field
                id="query"
                append-icon="mdi-content-copy"
                :value="stringQuery"
                solo
                readonly
                hide-details
                @click:append="copyQueryToClipboard"
              />
            </v-flex>
            <v-flex shrink>
              <v-btn
                color="success"
                @click="sendSearchQuery"
              >
                Search
              </v-btn>
            </v-flex>
          </v-layout>
          <v-layout
            column
            class="mt-2"
          >
            <v-flex>
              <v-card v-if="searchResults.length">
                <v-expansion-panel
                  v-model="resultsPanel"
                  expand
                >
                  <v-expansion-panel-content
                    v-for="(result, i) in searchResults"
                    :key="i"
                  >
                    <template v-slot:header>
                      <h1>{{ result.name }}</h1>
                    </template>
                    <v-card class="ma-3">
                      <VueJsonPretty
                        :data="result"
                        highlight-mouseover-node
                      />
                    </v-card>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-card>
            </v-flex>
            <v-spacer />
          </v-layout>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>

import VueJsonPretty from 'vue-json-pretty';

export default {
  name: 'QueryBuilder',
  inject: ['girderRest'],
  components: {
    VueJsonPretty,
  },
  data() {
    return {
      searchParams: [],
      searchResults: [],
      resultsPanel: [],
      rules: {
        number: val => this.validNumber(val) || 'Invalid Number',
        json: val => this.validJSON(val) || 'Invalid JSON',
      },
      selectedDateComparisonType: null,
      dateComparisonTypes: [
        {
          text: 'Greater Than (>)',
          value: '$gt',
        },
        {
          text: 'Greater Than/Equal To (≥)',
          value: '$gte',
        },
        {
          text: 'Less Than (<)',
          value: '$lt',
        },
        {
          text: 'Less Than/Equal To (≤	)',
          value: '$lte',
        },
        {
          text: 'Equal (=)',
          value: '$eq',
        },
        {
          text: 'Not Equal (≠)',
          value: '$ne',
        },
      ],
      paramTypes: [
        {
          label: 'String',
          value: 'string',
        },
        {
          label: 'Number',
          value: 'number',
        },
        {
          label: 'Date',
          value: 'date',
        },
        {
          label: 'JSON',
          value: 'json',
        },
      ],
      defaultParamType: 'string',
      error: false,
    };
  },
  computed: {
    query() {
      const reducer = (obj, param) => {
        let paramValue = param.value;
        if (param.type === 'number') paramValue = this.validNumber(paramValue) ? Number(paramValue) : paramValue;
        if (param.type === 'json') paramValue = this.validJSON(paramValue) ? JSON.parse(paramValue) : paramValue;
        if (param.type === 'date') {
          paramValue = {
            [this.selectedDateComparisonType]: paramValue,
          };
        }

        return {
          ...obj,
          [param.key]: paramValue,
        };
      };

      const query = this.searchParams
        .filter(x => x.key && x.value)
        .reduce(reducer, {});

      return query;
    },
    stringQuery() {
      return JSON.stringify(this.query);
    },
  },
  watch: {},
  methods: {
    validJSON(str) {
      try {
        JSON.parse(str);
      } catch (e) {
        return false;
      }
      return true;
    },
    validNumber(val) {
      return !Number.isNaN(Number(val));
    },
    selectDateComparisonType(val) {
      this.selectedDateComparisonType = val;
    },
    addSearchParam() {
      this.searchParams.push({
        key: '',
        value: '',
        type: this.defaultParamType,
      });
    },
    deleteSearchParam(index) {
      this.searchParams.splice(index, 1);
    },
    getRules(val) {
      const rules = [];
      if (val.type === 'number') rules.push(this.rules.number);
      if (val.type === 'json') rules.push(this.rules.json);

      return rules;
    },
    copyQueryToClipboard() {
      const queryField = document.querySelector('#query');
      queryField.select();
      document.execCommand('copy');
    },
    async sendSearchQuery() {
      try {
        const response = await this.girderRest.get('collection/geobrowser/search', {
          params: {
            query: this.query,
          },
        });
        this.searchResults = response.data;
      } catch (err) {
        this.searchResults = [];
      }
    },
  },
};
</script>
