import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

import { useSysMsgStore } from '@/stores/sysmsg'

export const useIsosStore = defineStore('isos', {
  
  state: () => ({
    items: [],
    sysMsg: useSysMsgStore()
  }),

  actions:{
    get_isos(){
      axios.get("/api/isos")
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

    get_iso_item_by_id(idx){
      const item = JSON.parse( JSON.stringify(this.items[idx]) )
      return item
    },

    add_iso(item){
      axios.post(`/api/iso`, item)
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

    edit_iso(item){
      const idx = this.items.findIndex(i => i.id === item.id)
      axios.put(`/api/iso/${item.id}`, item)
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

    delete_iso(idx){
      axios.delete(`/api/iso/${this.items[idx].id}`)
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
