import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

import { useSysMsgStore } from '@/stores/sysmsg'

export const useFilesStore = defineStore('files', {
  
  state: () => ({
    items: [],
    sysMsg: useSysMsgStore()
  }),

  actions:{
    get_files(){
      axios.get("/api/files")
      .then((response)=>{
        this.items = response.data
      })
      .catch((err)=>{
        console.error(err)
        this.sysMsg.alert = {
          message: err,
          dialog: true
        }
      })
    },

    get_file_item_by_id(idx){
      const item = JSON.parse( JSON.stringify(this.items[idx]) )
      item.data = atob(item.data)
      return item
    },

    add_file(item){
      item.data = btoa(item.data)
      axios.post(`/api/file`, item)
      .then((response)=>{
        this.items.push(response.data)
      })
      .catch((err)=>{
        console.error(err)
        this.sysMsg.alert = {
          message: err,
          dialog: true
        }
      })
    },

    edit_file(item){
      item.data = btoa(item.data)
      const idx = this.items.findIndex(i => i.id === item.id)
      axios.put(`/api/file/${item.id}`, item)
      .then((response)=>{
        this.items[idx] = item
      })
      .catch((err)=>{
        console.error(err)
        this.sysMsg.alert = {
          message: err,
          dialog: true
        }
      })
    },

    delete_file(idx){
      axios.delete(`/api/file/${this.items[idx].id}`)
      .then((response)=>{
        this.items.splice(idx, 1)
      })
      .catch((err)=>{
        console.error(err)
        this.sysMsg.alert = {
          message: err,
          dialog: true
        }
      })
    }

  }
})
