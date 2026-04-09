<template>
  <div class="d-flex justify-center mt-10">
    <v-card
      class="pa-3"
      title="Text Files" 
      width="90%"
    >
      <v-card-item>
        <div class="d-flex justify-end">
          <v-btn 
            class="ma-0 mr-5"
            density="compact" 
            icon="mdi-plus"
            color="blue-darken-2"
            @click="call_file_add"
          ></v-btn>
        </div>
        
        <v-data-table 
          :items="store.items" 
          :headers="filesHeaders" 
          :items-per-page="25" 
          :sort-by="[{ key: 'name', order: 'asc' }]"
        >
          <template #item.actions="{ item }">
            <div class="d-flex ga-2 justify-end">
              <v-icon 
                color="blue-darken-2" 
                icon="mdi-pencil" 
                size="small" 
                @click="call_file_edit(store.items.indexOf(item))"
              ></v-icon>
              <v-icon 
                color="blue-darken-2" 
                icon="mdi-content-copy" 
                size="small" 
                @click="call_file_copy(store.items.indexOf(item))"
              ></v-icon>
              <v-icon 
                color="blue-darken-2" 
                icon="mdi-download" 
                size="small" 
                @click="call_file_download(item.id)"
              ></v-icon>
              <v-icon 
                color="blue-darken-2" 
                icon="mdi-delete" 
                size="small" 
                @click="call_file_delete(store.items.indexOf(item))"
              ></v-icon>
            </div>
          </template>
        </v-data-table>
      </v-card-item>
    </v-card>

    <v-dialog v-model="fileAction.dialog" max-width="800" class="mb-14">
      <File :fileAction="fileAction" />
    </v-dialog>

  </div>
</template>


<script>
  import { useFilesStore } from '@/stores/files'
  import { useSysMsgStore } from '@/stores/sysmsg'

  import File from '@/components/File.vue'
  import Confirm from '@/components/Confirm.vue'

  export default{
    name: "Files",
    components:{
      File,
      Confirm
    },
    setup() {
      const store = useFilesStore()
      const sysMsg = useSysMsgStore()
      return {
        store,
        sysMsg
      }
    },
    data(){
      return {
        filesHeaders: [
          { title: 'Name', key: 'name', align: 'start' },
          { title: 'Id', key: 'id', align: 'start' },
          { title: 'Filename', key: 'filename', align: 'start' },
          { title: 'Comment', key: 'comment', align: 'start' },
          { title: 'Actions', key: 'actions', align: 'end', sortable: false },
        ],
        fileAction:{
          dialog: false,
          idx: null,
          mode: null
        },
      }
    },
    
    methods:{

      call_file_add(){
        this.fileAction = {
          idx: null,
          mode: "Add",
          dialog: true
        }
      },

      call_file_edit(idx){
        this.fileAction = {
          idx: idx,
          mode: "Edit",
          dialog: true
        }
      },

      call_file_copy(idx){
        this.fileAction = {
          idx: idx,
          mode: "Copy",
          dialog: true
        }
      },

      call_file_download(id){
        window.open(`/api/download/file/${id}`)
      },

      call_file_delete(idx){
        this.sysMsg.confirm = {
          dialog: true,
          message: `Do you really want to delete file "${this.store.items[idx].name}""`,
          callback: ()=>{ this.store.delete_file(idx) }
        }
      },

    },

    mounted(){
      this.store.get_files()
    }
  }
</script>


<style>
</style>