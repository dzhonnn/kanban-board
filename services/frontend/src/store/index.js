import { createStore } from 'vuex'

import notes from './modules/notes'
import users from './modules/users'
import sections from './modules/sections'

export default createStore({
  modules: {
    notes,
    users,
    sections,
  },
})
