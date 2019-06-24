<template>
  <v-layout>
    <v-textarea
      v-model="queryText"
      auto-grow
      box
      clearable
    />
    <v-textarea
      v-model="responseText"
      auto-grow
      box
      clearable
    />
  </v-layout>
</template>

<script>

export default {
  name: 'QueryBox',
  components: {},
  data() {
    return {
      queryText: '',
      responseText: '',
    };
  },
  computed: {},
  watch: {},
  methods: {},
};
</script>
