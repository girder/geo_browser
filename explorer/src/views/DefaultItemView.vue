<template>
  <div id="default-item-view">
    <v-card>
      {{ printedParams }}
    </v-card>
  </div>
</template>

<script>

export default {
  name: 'DefaultItemPage',
  components: {},
  data() {
    return {};
  },
  computed: {
    printedParams() {
      return JSON.stringify(this.$route.params, null, 4);
    },
  },
};
</script>

<style>
</style>
