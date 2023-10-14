<template>
  <div id="app">
    <header class="header">
      <h2 class="header-text">Sport Matches</h2>
    </header>
    <div class="line"></div>
    <div class="body">
      <form class="container form_styles container_login" v-if="login"  >
        <br>
        <h3>Sign In</h3>
        <br>
        <div class="col-12 form_col_width">
          <div class="form-label-group">
            <label for="inputEmail">Username</label>
            <input type="username" id="inputUsername" class="form-control"
                   placeholder="Username" required autofocus v-model="username">
          </div>
        </div>
        <br>
        <div class="col-12 form_col_width">
          <div class="form-label-group">
            <label for="inputPassword">Password</label>
            <input type="password" id="inputPassword" class="form-control"
                   placeholder="Password" required v-model="password">
          </div>
        </div>
        <br>
        <div class="col-12" >
          <button type="button" class="btn btn-primary buttons_login" @click="checkLogin">Sign In</button>
        </div>
        <br>
        <div class="col-12">
          <button type="button" class="btn btn-success buttons_login" @click="initCreateForm">Create Account</button>
        </div>
        <br>
        <div class="col-12" >
          <button type="button" class="btn btn-secondary buttons_login"  @click="toMatches">Back To Matches</button>
        </div>
        <br>
      </form>
      <form class="container form_styles container_login" v-if="!login"  >
        <br>
        <h3>Create Account</h3>
        <br>
        <div class="col-12 form_col_width">
          <div class="form-label-group">
            <label for="inputEmail">Username</label>
            <input type="username" id="inputUsername" class="form-control"
                   placeholder="Username" required autofocus v-model="addUserForm.username">
          </div>
        </div>
        <br>
        <div class="col-12 form_col_width">
          <div class="form-label-group">
            <label for="inputPassword">Password</label>
            <input type="password" id="inputPassword" class="form-control"
                   placeholder="Password" required v-model="addUserForm.password">
          </div>
        </div>
        <br>
        <div class="col-12" >
          <button type="button" class="btn btn-primary buttons_login" @click="createUser">Submit</button>
        </div>
        <br>
        <div class="col-12" >
          <button type="button" class="btn btn-secondary buttons_login"  @click="changLogin">Back To Log In</button>
        </div>
        <br>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      host: 'localhost:8000',
      login: true,
      logged: false,
      username: null,
      password: null,
      token: null,
      addUserForm: {
        username: null,
        password: null
      }
    }
  },
  methods: {
    changLogin () {
      this.login = !this.login
    },
    checkLogin () {
      const encodedUsername = encodeURIComponent(this.username)
      const encodedPassword = encodeURIComponent(this.password)
      const parameters = 'username=' + encodedUsername + '&password=' + encodedPassword
      const config = {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
      const path = 'http://' + this.host + '/login'
      axios.post(path, parameters, config)
        .then((res) => {
          this.logged = true
          this.token = res.data.access_token
          this.$router.push({ path: '/', query: { username: this.username, logged: this.logged, token: this.token } })
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          alert('El nombre de usario o la contraseña es incorrecta.')
        })
    },
    toMatches () {
      this.$router.push({ path: '/' })
    },
    initCreateForm () {
      this.changLogin()
      this.addUserForm.username = null
      this.addUserForm.password = null
    },
    createUser () {
      if (this.addUserForm.username == null && this.addUserForm.password == null) {
        alert('El campo de nombre de usuario o contraseña está vacío.')
      } else {
        const path = 'http://' + this.host + '/account'
        const parameters = {
          username: this.addUserForm.username,
          password: this.addUserForm.password,
          available_money: 100.0,
          is_admin: 0
        }
        axios.post(path, parameters)
          .then(() => {
            console.log('Account created')
            alert('Cuenta creada!')
          })
          .catch((error) => {
            console.log(error)
            if (this.addUserForm.password.length < 8) {
              alert('La contraseña es demasiado corta. Mínimo 8 caracteres')
            } else if (this.addUserForm.password.length > 24) {
              alert('La contraseña es demasiado larga. Máximo 24 caracteres')
            } else {
              alert('El nombre de usuario no está disponible')
            }
          })
      }
    }
  }

}
</script>

<style>
#app {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
/* Estilos del header */
.header {
  background-color: white;
  padding: 20px;
}

.header-text {
  margin-left: 100px;
  color: black;
  font-size: xxx-large;
  text-align: left;
}

/* Estilos del cuerpo */
.body {
  background-color: beige;
  padding: 20px;
}
.line {
  height: 2px;
  background-color: gray;
}
.container_login{
  width: 500px;
  height: auto;
  background-color: white;
  border: 1px solid gray;
  border-radius: 5px;
}
.form_styles{
  align-content: center;
  justify-content: center;
  align-items: center;
  width: 400px;
}
.form_col_width{
  display: flex;
  align-content: center;
  justify-content: center;
  align-items: center;
  width: 350px;
}
.buttons_login{
  width: 350px;
}
.form-label-group {
  text-align: left;
}
</style>
