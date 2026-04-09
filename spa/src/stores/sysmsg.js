import { defineStore } from 'pinia'

export const useSysMsgStore = defineStore('sysmsg', {
  
  state: () => ({
    alert: {
      dialog: false,
      message: null,
    },
    confirm: {
      dialog: false,
      message: null,
      callback: ()=>{},
    }
  }),

  actions:{
    resetAlert(){
      this.alert = {
        dialog: false,
        message: null,
      }
    },
    resetConfirm(){
      this.confirm = {
        dialog: false,
        message: null,
        callback: ()=>{},
      }
    }
  }

})