<template>
  <div id="main-page">
    <v-container>
      <v-layout>
        <v-flex xs8>
          <CollectionMap class="collection-map" />
        </v-flex>
        <v-flex
          xs4
          class="data-browser-container"
        >
          <DataBrowser :location.sync="location" />
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>

import { DataBrowser } from '@girder/components/src/components';
import CollectionMap from '@/components/CollectionMap.vue';

export default {
  name: 'MainPage',
  components: {
    CollectionMap,
    DataBrowser,
  },
  data() {
    return {
      browserLocation: null,
    };
  },
  inject: ['girderRest'],
  computed: {
    location: {
      get() {
        if (this.browserLocation) {
          return this.browserLocation;
        }
        return { type: 'collections' };
      },
      set(newVal) {
        this.browserLocation = newVal;
      },
    },
  },
  watch: {},
  methods: {},
};
</script>

<style>
.collection-map {
  margin-left: 3%;
  margin-right: 3%;
  height: 700px;
}

.data-browser-container {
  text-align: left;
}
</style>
