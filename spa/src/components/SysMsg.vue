<script setup>
import { useSysMsgStore } from '@/stores/sysmsg'
const sysMsgStore = useSysMsgStore()

</script>

<template>
  <div>
    <v-dialog v-model="sysMsgStore.alert.dialog" max-width="400" class="mb-14"> 
      <v-card v-if="sysMsgStore.alert.dialog" title="System message - Alert"> 
        <v-card-text>
          {{ sysMsgStore.alert.message }}
        </v-card-text>
        <v-card-text class="d-flex justify-center">
          <v-btn 
            min-width="100" 
            class="mb-2 
            mx-2"
            @click="sysMsgStore.resetAlert">Ok</v-btn>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="sysMsgStore.confirm.dialog" max-width="400" class="mb-14"> 
      <v-card v-if="sysMsgStore.confirm.dialog" title="System message - Confirm"> 
        <v-card-text>
          {{ sysMsgStore.confirm.message }}
        </v-card-text>
        <v-card-text class="d-flex justify-center">
          <v-btn 
            min-width="100" 
            class="mb-2 mx-2" 
            color="blue-darken-2"
            @click="sysMsgStore.confirm.callback(); sysMsgStore.resetConfirm()">Ok</v-btn>
          <v-btn 
            min-width="100" 
            class="mb-2 
            mx-2"
            @click="sysMsgStore.resetConfirm">Cancel</v-btn>
        </v-card-text>
      </v-card>
    </v-dialog>


  </div>
</template>