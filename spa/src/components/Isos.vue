<template>
  <div class="d-flex justify-center mt-10">
    <v-card
      class="pa-3"
      title="Isos" 
      width="90%"
    >
      <v-card-item>
        <div class="d-flex justify-end">
          <v-btn 
            class="ma-0 mr-5"
            density="compact" 
            icon="mdi-plus"
            color="blue-darken-2"
            @click="call_iso_add"
          ></v-btn>
        </div>

        <v-data-table 
          :items="store.items" 
          :headers="isosHeaders" 
          :items-per-page="25" 
          :sort-by="[{ key: 'name', order: 'asc' }]"
        >
          <template #item.actions="{ item }">
            <div class="d-flex ga-2 justify-end">
              <v-icon 
                color="blue-darken-2" 
                icon="mdi-pencil" 
                size="small" 
                @click="call_iso_edit(store.items.indexOf(item))"
              ></v-icon>
              <v-icon 
                color="blue-darken-2" 
                icon="mdi-download" 
                size="small" 
                @click="call_iso_download(item.id)"
              ></v-icon>
              <v-icon 
                color="blue-darken-2" 
                icon="mdi-delete" 
                size="small" 
                @click="call_iso_delete(store.items.indexOf(item))"
              ></v-icon>
            </div>
          </template>
        </v-data-table>
      </v-card-item>
    </v-card>

    <v-dialog v-model="isoAction.dialog" width="70%" min-width="800" class="mb-14">
      <Iso :isoAction="isoAction" />
    </v-dialog>

  </div>
</template>


<script>
  import { useIsosStore } from '@/stores/isos'
  import { useSysMsgStore } from '@/stores/sysmsg'

  import Iso from '@/components/Iso.vue'
  import Confirm from '@/components/Confirm.vue'

  export default{
    name: "Isos",
    components:{
      Iso,
      Confirm
    },
    setup() {
      const store = useIsosStore()
      const sysMsg = useSysMsgStore()
      return {
        store,
        sysMsg
      }
    },
    data(){
      return {
        isosHeaders: [
          { title: 'Name', key: 'name', align: 'start' },
          { title: 'Id', key: 'id', align: 'start' },
          { title: 'Label', key: 'label', align: 'start' },
          { title: 'Comment', key: 'comment', align: 'start' },
          { title: 'Actions', key: 'actions', align: 'end', sortable: false },
        ],
        isoAction:{
          dialog: false,
          idx: null,
          mode: null
        },
      }
    },

    methods:{

      call_iso_add(){
        this.isoAction = {
          idx: null,
          mode: "Add",
          dialog: true
        }
      },

      call_iso_edit(idx){
        this.isoAction = {
          idx: idx,
          mode: "Edit",
          dialog: true
        }
      },

      call_iso_download(id){
        window.open(`/api/download/iso/${id}`)
      },

      call_iso_delete(idx){
        this.sysMsg.confirm = {
          dialog: true,
          message: `Do you really want to delete iso "${this.store.items[idx].name}""`,
          callback: ()=>{ this.store.delete_iso(idx) }
        }
      },
      
    },
    mounted(){
      this.store.get_isos()
    }
  }
</script>


<style>
</style>