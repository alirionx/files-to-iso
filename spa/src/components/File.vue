<template>
  <v-card :title="`${fileAction.mode} ${item.name}`"> 
    <v-card-text>
      <v-form >
          <v-row class="ma-0">
            <v-col cols="12" sm="6">
              <v-text-field v-model="item.id" label="Id" disabled></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="item.name" label="Name"></v-text-field>
            </v-col>
          </v-row>
          <v-row class="ma-0">
            <v-col cols="12" sm="6">
              <v-text-field v-model="item.filename" label="Filename"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="item.comment" label="Comment"></v-text-field>
            </v-col>
          </v-row>
          <v-row class="ma-0">
            <v-textarea label="data" style="min-height: 400px;" v-model="item.data"></v-textarea>
          </v-row>
          <v-row class="ma-0">
            <v-btn 
              min-width="100" 
              class="mb-2 mx-2" 
              color="blue-darken-2"
              @click="submit">Submit</v-btn>
            <v-btn 
              min-width="100" 
              class="mb-2 
              mx-2"
              @click="reset">Cancel</v-btn>
          </v-row>
      </v-form>    
    </v-card-text>
  </v-card>
</template>


<script>
  import { useFilesStore } from '@/stores/files'

  export default{
    name: "File",
    components:{
    },
    setup() {
      const store = useFilesStore()
      return {
        store
      }
    },
    props: {
      fileAction: Object,
    },
    data(){
      return {
        item: {},
      }
    },
    methods:{

      submit(){
        if(this.fileAction.mode == "Edit"){
          this.store.edit_file(this.item)
        }
        else{
          this.store.add_file(this.item)
        }
        this.reset()
      },

      reset(){
        this.fileAction.dialog = false
        this.fileAction.idx = false
        this.fileAction.mode = null
      }

    },

    mounted(){
      if(this.fileAction.mode != "Add"){
        // this.get_file()
        this.item = this.store.get_file_item_by_id(this.fileAction.idx)
        if(this.fileAction.mode == "Copy"){
          delete(this.item.id)
          this.item.name = this.item.name + " - copy"
        }
      }
    }
  }
</script>
