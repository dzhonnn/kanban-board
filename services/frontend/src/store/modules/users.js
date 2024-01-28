import axios from 'axios'

const state = {
  user: null,
}

const getters = {
  isAuthenticated: (state) => !!state.user,
  stateUser: (state) => state.user,
}

const actions = {
  // eslint-disable-next-line no-empty-pattern
  async register({}, form) {
    await axios.post('register', form)
    // await dispatch('logIn', userForm)
  },
  async logIn({ dispatch }, form) {
    console.log(form)
    console.log(form.email)
    console.log(form.password)
    const email = form.email
    const password = form.password
    await axios.post(`login?email=${email}&password=${password}`)
    await dispatch('viewMe')
  },
  async viewMe({ commit }) {
    let { data } = await axios.get('users/whoami')
    await commit('setUser', data)
  },
  async deleteUser(id) {
    await axios.delete(`user/${id}`)
  },
  async logOut({ commit }) {
    let user = null
    commit('logout', user)
  },
  // eslint-disable-next-line no-empty-pattern
  async reset({}, email) {
    await axios.post(`forgot_password?email=${email}`)
  },
  // eslint-disable-next-line no-empty-pattern
  async resetPass({}, form) {
    let newForm = new FormData()
    newForm.append('new_password', form.new_password)
    await axios.post(
      `reset_password?access_token=${form.access_token}`,
      newForm
    )
  },
  async exportBoard() {
    await axios.post('user/export_send')
    await axios.get('user/export_get').then((response) => {
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'board.xml')
      document.body.appendChild(link)
      link.click()
    })
  },
}

const mutations = {
  setUser(state, username) {
    state.user = username
  },
  logout(state, user) {
    state.user = user
  },
}

export default {
  state,
  getters,
  actions,
  mutations,
}
