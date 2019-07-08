<template>
  <v-container>
    <v-layout row>
      <v-flex
        xs3
        class="ma-1"
      >
        <v-layout column>
          <v-card>
            <h1>Search Filters</h1>
            <v-flex
              v-for="(param, i) in searchParams"
              :key="i"
            >
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
                <v-flex grow>
                  <v-card
                    class="ma-2"
                    flat
                  >
                    <v-text-field
                      v-model="param.key"
                      label="Key"
                      hide-details
                      solo
                    />
                    <v-text-field
                      v-model="param.value"
                      label="Value"
                      solo
                      :rules="getRules(param)"
                    />
                  </v-card>
                </v-flex>
              </v-layout>
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
                :value="query"
                solo
                readonly
                hide-details
                @click:append="copyQueryToClipboard"
              />
            </v-flex>
            <v-flex shrink>
              <v-btn
                color="success"
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
                <v-list>
                </v-list>
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

export default {
  name: 'QueryBuilder',
  inject: ['girderRest'],
  data() {
    return {
      searchParams: [],
      searchResults: [],
      rules: {
        number: val => !/[a-zA-Z]/.test(val) || 'Number cannot contain alphabetical characters',
      },
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
      ],
      defaultParamType: 'string',
      error: false,
    };
  },
  computed: {
    query() {
      const query = this.searchParams
        .filter(x => x.key && x.value)
        .reduce((obj, param) => {
          let paramValue = param.value;
          if (param.type === 'number') paramValue = Number(paramValue);
          // if (param.type === 'date') paramValue =
          return {
            ...obj,
            [param.key]: paramValue,
          };
        }, {});

      return JSON.stringify(query);
    },
  },
  watch: {},
  methods: {
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
      if (val.type === 'number') return [this.rules.number];
      return [];
    },
    copyQueryToClipboard() {
      const queryField = document.querySelector('#query');
      queryField.select();
      document.execCommand('copy');
    },
  },
};
</script>
