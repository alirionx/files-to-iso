<template>
  <v-card :title="`${isoAction.mode} ${item.name}`"> 
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
              <v-text-field v-model="item.label" label="Label"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="item.comment" label="Comment"></v-text-field>
            </v-col>
          </v-row>

          <v-row class="ma-0">
            <v-container class="mt-6 mb-0 px-2 py-0 d-flex justify-space-between align-center">
              <span style="font-weight: bold;">Assigned Text Files</span>
              <v-btn 
                class="ma-0 mr-5"
                density="compact" 
                icon="mdi-plus"
                color="blue-darken-2"
                @click="tfaDialog=true"
              ></v-btn>
            </v-container>
            
            <v-table density="compact" class="mt-0 mb-8 w-100">
              <thead>
                <tr>
                  <th class="text-left">Name</th>
                  <th class="text-left">Filename</th>
                  <th class="text-left">Id</th>
                  <th class="text-left">Path</th>
                  <th class="text-center">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(tf, idx) in item.text_files" :key="tf.id" >
                  <td>{{ get_file_by_id(tf.id).name }}</td>
                  <td>{{ get_file_by_id(tf.id).filename }}</td>
                  <td>{{ tf.id }}</td>
                  <td >
                    <input type="text" class="tableIpt" v-model="tf.path" />
                    <!-- <v-text-field  v-model="tf.path" min-width="260px" density="compact"></v-text-field> -->
                  </td>
                  <td class="text-center">
                    <v-icon 
                      color="blue-darken-2" 
                      icon="mdi-delete" 
                      @click="unassign_textfile(idx)"
                    ></v-icon>
                  </td>
                </tr>
              </tbody>
            </v-table>
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
    
    <v-dialog v-model="tfaDialog" width="68%" max-width="1200" class="mb-14">
      <v-card class="pa-4">
        <v-table density="compact" class="">
          <thead>
            <tr>
              <th class="text-left">Name</th>
              <th class="text-left">Filename</th>
              <th class="text-left">Id</th>
              <th class="text-left">Comment</th>
              <th class="text-right">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(tf, idx) in filesStore.items" :key="tf.id" >
              <td>{{ tf.name }}</td>
              <td>{{ tf.filename }}</td>
              <td>{{ tf.id }}</td>
              <td>{{ tf.comment }}</td>
              <td class="text-right">
                <v-icon 
                  v-if="is_in_tf(idx)" 
                  color="green-darken-3" 
                  icon="mdi-check" 
                ></v-icon>
                <v-icon 
                  color="blue-darken-3" 
                  icon="mdi-plus" 
                  @click="textfile_add(idx)"
                ></v-icon>
              </td>
            </tr>
          </tbody>
        </v-table>
        <v-btn 
          width="100" 
          class="ma-2 mt-4"
          @click="tfaDialog=false"
        >Close</v-btn>
      </v-card>
    </v-dialog>

  </v-card>
</template>

<script>
  import { useFilesStore } from '@/stores/files'
  import { useIsosStore } from '@/stores/isos'

  export default{
    name: "Iso",
    components:{
    },
    props: {
      isoAction: Object,
    },
    setup() {
      const isosStore = useIsosStore()
      const filesStore = useFilesStore()
      return {
        isosStore,
        filesStore
      }
    },
    data(){
      return {
        item: {
          text_files:[]
        },
        tfaDialog: false
      }
    },
    methods:{
      get_files(){
        axios.get("/api/files")
        .then((response)=>{
          this.files = response.data
        })
        .catch((err)=>{
          console.error(err)
        })
        .finally(()=>{
        })
      },

      get_file_by_id(id){
        const file = this.filesStore.items.find(item => item.id === id)
        return file
      },

      unassign_textfile(idx){
        this.item.text_files.splice(idx, 1)
      },

      is_in_tf(idx){
        const chk = this.item.text_files.find(item => item.id === this.filesStore.items[idx].id)
        if(chk){
          return true
        }
        else{
          return false
        }
      },
      
      textfile_add(idx){
        const fta = {
          id: this.filesStore.items[idx].id,
          path: "/"
        }

        console.log(fta)
        this.item.text_files.push(fta)
      },


      submit(){
        if(this.isoAction.mode == "Edit"){
          this.isosStore.edit_iso(this.item)
        }
        else{
          this.isosStore.add_iso(this.item)
        }
        this.reset()
      },

      reset(){
        this.isoAction.dialog = false
        this.isoAction.idx = false
        this.isoAction.mode = null
      }

    },

    mounted(){
      if(this.isoAction.mode != "Add"){
        this.item = this.isosStore.get_iso_item_by_id(this.isoAction.idx)
      }
    }
  }
</script>


<style scoped>
.tableIpt{
  border: none;
  background-color: rgb(240, 240, 240);
  padding: 6px;
  margin: 6px;
  min-width: 240px;
}
</style>