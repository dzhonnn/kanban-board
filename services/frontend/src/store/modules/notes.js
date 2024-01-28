import axios from 'axios'

const state = {
  notes: null,
  note: null,
}

const getters = {
  stateNotes: (state) => state.notes,
  stateNote: (state) => state.note,
}

const actions = {
  // eslint-disable-next-line no-empty-pattern
  async createNote({}, note) {
    await axios.post('note', note)
  },
  // eslint-disable-next-line no-empty-pattern
  async updateNote({}, note) {
    await axios.patch(`note/${note.id}`, note.form)
  },
  // eslint-disable-next-line no-empty-pattern
  async deleteNote({}, id) {
    await axios.delete(`note/${id}`)
  },
}

const mutations = {
  setNotes(state, notes) {
    state.notes = notes
  },
  setNote(state, note) {
    state.note = note
  },
}

export default {
  state,
  getters,
  actions,
  mutations,
}
