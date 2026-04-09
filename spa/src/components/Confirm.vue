<script setup>
const props = defineProps({
  confirm: Object
})
</script>

<template>
  <v-card title="System message - Confirm"> 
    <v-card-text>
      {{ confirm.message }}
    </v-card-text>
    <v-card-text class="d-flex justify-center">
      <v-btn 
        min-width="100" 
        class="mb-2 mx-2" 
        color="blue-darken-2"
        @click="confirm.callback">Ok</v-btn>
      <v-btn 
        min-width="100" 
        class="mb-2 
        mx-2"
        @click="confirm.reset">Cancel</v-btn>
    </v-card-text>
  </v-card>
</template>

