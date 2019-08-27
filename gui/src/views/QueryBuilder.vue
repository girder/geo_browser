<template>
  <v-container>
    <v-layout row>
      <v-flex
        xs3
        class="ma-1"
      >
        <v-layout column>
          <v-layout>
            <v-flex>
              <h1>Collection Search Builder</h1>
            </v-flex>
            <v-flex>
              <v-dialog>
                <template v-slot:activator="{ on }">
                  <v-btn
                    icon
                    v-on="on"
                  >
                    <v-icon>mdi-help-circle</v-icon>
                  </v-btn>
                </template>
                <v-card class="text-xs-left">
                  <MarkdownViewer :text="helpPageText" />
                </v-card>
              </v-dialog>
            </v-flex>
          </v-layout>
          <v-card>
            <v-layout>
              <v-flex xs11>
                <h1 class="text-xs-left mx-2">
                  Search Filters
                </h1>
              </v-flex>
              <v-flex v-if="searchParams.length">
                <v-btn
                  icon
                  @click="searchParams = []"
                >
                  <v-icon>mdi-notification-clear-all</v-icon>
                </v-btn>
              </v-flex>
            </v-layout>
            <v-list>
              <v-list-tile
                v-for="(param, i) in searchParams"
                :key="i"
              >
                <v-list-tile-content>
                  <v-list-tile-title>
                    {{ param.key }}: {{ param.value }}
                  </v-list-tile-title>
                  <v-list-tile-sub-title>
                    {{ param.type }}
                  </v-list-tile-sub-title>
                </v-list-tile-content>
                <v-list-tile-action>
                  <v-btn
                    icon
                    ripple
                    @click="deleteSearchParam(i)"
                  >
                    <v-icon color="error">
                      mdi-delete
                    </v-icon>
                  </v-btn>
                </v-list-tile-action>
              </v-list-tile>
            </v-list>
            <v-flex>
              <v-dialog v-model="addItemDialog">
                <v-card class="my-1">
                  <v-layout column>
                    <v-flex shrink>
                      <v-layout
                        class="mx-2"
                        align-center
                        row
                      >
                        <v-radio-group
                          v-model="newSearchParam.type"
                          row
                        >
                          <v-radio
                            v-for="(type, j) in paramTypes"
                            :key="j"
                            :label="type.label"
                            :value="type.value"
                          />
                        </v-radio-group>
                      </v-layout>
                    </v-flex>
                    <v-flex
                      grow
                      class="ma-2"
                    >
                      <v-card flat>
                        <template v-if="newSearchParam.type === 'json'">
                          <v-textarea
                            v-model="newSearchParam.value"
                            :rules="getRules(newSearchParam)"
                            box
                          />
                        </template>
                        <template v-else>
                          <v-text-field
                            v-model="newSearchParam.key"
                            label="Key"
                            :rules="keyRules"
                          />
                          <v-text-field
                            v-if="newSearchParam.type !== 'date'"
                            v-model="newSearchParam.value"
                            label="Value"
                            :rules="getRules(newSearchParam)"
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
                              v-model="newSearchParam.dateMenu"
                              :close-on-content-click="false"
                              lazy
                              transition="scale-transition"
                              offset-y
                              full-width
                              min-width="290px"
                            >
                              <template v-slot:activator="{ on }">
                                <v-text-field
                                  v-model="newSearchParam.value"
                                  label="Date"
                                  hide-details
                                  prepend-inner-icon="mdi-calendar"
                                  v-on="on"
                                />
                              </template>
                              <v-date-picker
                                v-model="newSearchParam.value"
                                no-title
                                scrollable
                              >
                                <v-spacer />
                                <v-btn
                                  flat
                                  color="primary"
                                  @click="newSearchParam.dateMenu = false"
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-flex>
                        </template>
                      </v-card>
                    </v-flex>
                    <v-layout>
                      <v-flex shrink>
                        <v-btn
                          color="secondary"
                          @click="cancelSearchParam"
                        >
                          Cancel
                        </v-btn>
                      </v-flex>
                      <v-flex shrink>
                        <v-btn
                          color="success"
                          @click="addSearchParam"
                        >
                          Add
                        </v-btn>
                      </v-flex>
                    </v-layout>
                  </v-layout>
                </v-card>
              </v-dialog>
              <v-btn
                color="secondary"
                @click="clickAddItem"
              >
                <v-icon>mdi-plus</v-icon>
                Add Item
              </v-btn>
              <v-btn
                color="success"
                :disabled="internalQuery === activeQuery"
                @click="applyAndSearch"
              >
                Apply
              </v-btn>
            </v-flex>
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
            <v-flex>
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
import MarkdownViewer from '@girder/components/src/components/Markdown.vue';
import HelpPage from '@/assets/QueryHelpPage.md';

export default {
  name: 'QueryBuilder',
  inject: ['girderRest'],
  components: {
    VueJsonPretty,
    MarkdownViewer,
  },
  data() {
    return {
      helpPageText: HelpPage,
      searchParams: [],
      searchResults: [],
      resultsPanel: [],
      activeQuery: '',
      newSearchParam: {},
      addItemDialog: false,
      keyRules: [
        key => key.length > 0 || 'Required',
      ],
      valueRules: {
        number: val => this.validNumber(val) || 'Invalid Number',
        json: val => this.validJSON(val) || 'Invalid JSON',
        any: val => !!val || 'Required',
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
          text: 'Less Than/Equal To (≤)',
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
      defaultSearchParam: {
        key: '',
        value: '',
        type: 'string',
      },
      error: false,
    };
  },
  computed: {
    internalQuery() {
      const filter = x => (x.key && x.value) || x.type === 'json';
      const reducer = (obj, param) => {
        let paramValue = param.value;
        if (param.type === 'number') paramValue = this.validNumber(paramValue) ? Number(paramValue) : paramValue;
        if (param.type === 'json' && this.validJSON(paramValue)) {
          paramValue = JSON.parse(paramValue);
          return {
            ...obj,
            ...paramValue,
          };
        }

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
        .filter(filter)
        .reduce(reducer, {});

      return query;
    },
    stringQuery() {
      if (!this.activeQuery) return this.activeQuery;
      return JSON.stringify(this.activeQuery);
    },
    validSearchParamKey() {
      return !this.keyRules.filter(x => typeof x(this.newSearchParam.key) === 'string').length;
    },
    validSearchParamValue() {
      const rules = this.getRules(this.newSearchParam);
      const errors = rules.filter(x => typeof x(this.newSearchParam.value) === 'string');
      return errors.length === 0;
    },
  },
  watch: {},
  created() {
    this.newSearchParam = { ...this.defaultSearchParam };
  },
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
    clickAddItem() {
      this.addItemDialog = true;
    },
    addSearchParam() {
      if (
        !this.validSearchParamValue
        || (!this.validSearchParamKey && this.newSearchParam.type !== 'json')
      ) return;
      this.searchParams.push(this.newSearchParam);
      this.newSearchParam = { ...this.defaultSearchParam };
      this.addItemDialog = false;
    },
    deleteSearchParam(index) {
      this.searchParams.splice(index, 1);
    },
    cancelSearchParam() {
      this.newSearchParam = { ...this.defaultSearchParam };
      this.addItemDialog = false;
    },
    getRules(val) {
      const rules = [];
      if (val.type === 'number') rules.push(this.valueRules.number);
      if (val.type === 'json') rules.push(this.valueRules.json);
      rules.push(this.valueRules.any);

      return rules;
    },
    copyQueryToClipboard() {
      const queryField = document.querySelector('#query');
      queryField.select();
      document.execCommand('copy');
    },
    async applyAndSearch() {
      this.activeQuery = this.internalQuery;
      try {
        const response = await this.girderRest.get('collection/geobrowser/search', {
          params: {
            query: this.activeQuery,
          },
        });
        this.searchResults = response.data;
      } catch (err) {
        this.searchResults = [];
      } finally {
        this.resultsPanel = [];
      }
    },
  },
};
</script>
