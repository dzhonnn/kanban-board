import axios from 'axios'

const state = {
  sections: null,
  section: null,
}

const getters = {
  stateSections: (state) => state.sections,
  stateSection: (state) => state.section,
}

const actions = {
  async createSection({ dispatch }, section) {
    await axios.post('section', section)
    await dispatch('getSections')
  },
  async getSections({ commit }) {
    let { data } = await axios.get('sections')
    commit('setSections', data)
  },
  // eslint-disable-next-line no-empty-pattern
  async updateSection({}, section) {
    await axios.patch(`sections/${section.id}`, section.form)
  },
  // eslint-disable-next-line no-empty-pattern
  async deleteSection({}, id) {
    await axios.delete(`sections/${id}`)
  },
}

const mutations = {
  setSections(state, sections) {
    state.sections = sections
  },
  setSection(state, section) {
    state.section = section
  },
}

export default {
  state,
  getters,
  actions,
  mutations,
}
