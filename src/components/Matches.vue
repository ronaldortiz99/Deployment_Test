<template>
    <div id="app">
      <header class="header">
        <div class="row" >
          <div class="col-8">
            <h2 class="header-text">{{ message }}</h2>
          </div>
          <div class="col-4 contendor" v-if="logged" >
            <span class="margen">{{username}}</span>
            <span class="material-icons margen" style="color: gray; background-color: transparent">person</span>
            <span class="margen">{{total_money.toFixed(2)}}</span>
            <span class="material-icons margen" style="color: green; background-color: transparent">euro</span>
            <button class="btn btn-outline-primary align-items-center margen" style="display: flex;" @click="veureCistella()">
              <span>{{ msgCistella }}</span>
              <span class="notificacion">{{matches_added.length}}</span>
            </button>
            <button class="btn btn-outline-success margen" @click="getHistorial" v-if="!historial">Historial</button>
            <button class="btn btn-outline-success margen" @click="logOut">Log Out</button>
          </div>
          <div class="col-4 contendor" v-if="!logged">
            <button class="btn btn-outline-primary margen" @click="logIn">Log In</button>
          </div>
        </div>
      </header>
      <div class="line"></div>
      <div class="body">
        <div class="container">
          <div class="row" style="margin-top: 20px" v-if="!cistella" >
            <div class="col-lg-4 col-md-6 mb-4" v-for="(match) in matches" :key="match.id">
              <div class="card" style="width: 18rem;">
                <img class="card-img-top" style="height: 200px" :src="images[match.competition.sport]" alt="Card image cap">
                <div class="card-body">
                  <h5>{{ match.competition.sport }} - {{ match.competition.category }}</h5>
                  <h6>{{ match.competition.name }}</h6>
                  <h6><strong>{{ match.local.name }}</strong> ({{ match.local.country }}) vs <strong>{{ match.visitor.name }}</strong> ({{ match.visitor.country }})</h6>
                  <h6>Data: {{ match.date.substring(0,10) }}</h6>
                  <h6>Preu: {{ match.price }} &euro;</h6>
                  <h6>Tickets disponibles: {{ match.total_available_tickets}}</h6>
                  <button class="btn btn-success btn-lg" @click="addEventToCart(match)" :disabled="buy(match)"> Afegeix a la cistella </button>
                </div>
              </div>
            </div>
          </div>
          <div v-if="cistella">
            <div v-if="!historial">
              <table class="table caption-top">
                <thead>
                <tr>
                  <th scope="col">Sport</th>
                  <th scope="col">Competition</th>
                  <th scope="col">Match</th>
                  <th scope="col">Quantity</th>
                  <th scope="col">Price(&euro;)</th>
                  <th scope="col">Total(&euro;)</th>
                  <th scope="col"></th>
                </tr>
                </thead>
                <tbody v-for="(match) in matches_added" :key="match.id">
                <td>{{match.competition.sport}}</td>
                <td>{{match.competition.name}}</td>
                <td>{{match.local.name}} VS {{match.visitor.name}}</td>
                <td>
                  {{match.quantity}}
                  <button type="button" class="btn btn-success" style="width: 40px; font-weight: bold" :disabled="buy(match)" @click="addEventToCart(match)">+</button>
                  <button type="button" class="btn btn-danger" style="width: 40px; font-weight: bold" @click="subEventToCart(match)">-</button>
                </td>
                <td>{{match.price}}</td>
                <td>{{(match.price * match.quantity).toFixed(2)}}</td>
                <td><button type="button" class="btn btn-danger" style=" font-weight: bold" @click="removeEventToCart(match)">Eliminar</button></td>
                </tbody>
              </table>
            </div>
            <div v-if="historial">
              <table class="table caption-top">
                <thead>
                <tr>
                  <th scope="col">Sport</th>
                  <th scope="col">Competition</th>
                  <th scope="col">Match</th>
                  <th scope="col">Quantity</th>
                  <th scope="col">Price(&euro;)</th>
                  <th scope="col">Total(&euro;)</th>
                  <th scope="col"></th>
                </tr>
                </thead>
                <tbody v-for="(ord) in order" :key="ord.id">
                <td>{{ord.sport}}</td>
                <td>{{ord.competition}}</td>
                <td>{{ord.local}} VS {{ord.visitor}}</td>
                <td>{{ord.tickets_bought}}</td>
                <td>{{ord.price}}</td>
                <td>{{(ord.price * ord.tickets_bought).toFixed(2)}}</td>
                </tbody>
              </table>
            </div>
            <button type="button" class="btn btn-secondary" style="font-weight: bold" @click="actEnrere()" v-if="!historial">Enrere</button>
            <button type="button" class="btn btn-success" :disabled="purchase()" style="font-weight: bold" @click="finalizePurchase()" v-if="!historial">Finalitzar la compra</button>
          </div>
        </div>
      </div>
    </div>
  </template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      cistella: false,
      historial: false,
      msgCistella: 'Cistella',
      host: 'localhost:8000',
      images: {
        'Volleyball': './static/img/volei.jpg',
        'Futsal': './static/img/futsal.jpg',
        'Football': './static/img/futbol.jpg',
        'Basketball': './static/img/basket.jpg'
      },
      order: [],
      matches_added: [],
      matches: [],
      message: 'Sport Matches',
      total_money: 0,
      money_available: 0,
      tickets_bought: 0,
      logged: false,
      username: null,
      is_admin: null,
      token: null
    }
  },
  created () {
    this.logged = this.$route.query.logged === 'true'
    this.username = this.$route.query.username
    this.token = this.$route.query.token
    if (this.logged === undefined) {
      this.logged = false
    }
    this.getAccount()
    this.getMatches()
    this.getOrders()
  },
  methods: {
    getHistorial () {
      this.cistella = true
      this.historial = true
      for (let i = 0; i < this.order.length; i += 1) {
        for (let j = 0; j < this.matches.length; j += 1) {
          if (this.matches[j].id === this.order[i].match_id) {
            var match = this.matches[j]
            this.order[i].local = match.local.name
            this.order[i].local = match.visitor.name
            this.order[i].competition = match.competition.name
            this.order[i].sport = match.competition.sport
            this.order[i].price = match.price
          }
        }
      }
    },
    getOrders () {
      const path = 'http://' + this.host + `/orders/${this.username}`
      axios.get(path, {
        headers: {
          Authorization: 'Bearer ' + this.token
        }
      }).then((res) => {
        this.order = res.data
      })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    },
    actEnrere () {
      this.getOrders()
      this.getMatches()
      this.veureCistella()
    },
    logIn () {
      this.$router.push({ path: '/userLogin' })
    },
    logOut () {
      this.cistella = false
      this.logged = false
      this.token = null
      this.username = null
      this.total_money = 0
      this.money_available = 0
      this.$router.push({ path: '/' })
    },
    veureCistella () {
      if (this.historial) {
        this.historial = false
      } else {
        this.cistella = !this.cistella
        if (!this.cistella) {
          this.msgCistella = 'Cistella'
          this.historial = false
        } else {
          this.msgCistella = 'Tancar cistella'
          this.historial = false
        }
      }
    },
    getMatches () {
      const pathMatches = 'http://' + this.host + '/matches/'
      axios.get(pathMatches)
        .then((res) => {
          var matches = res.data.filter((match) => {
            return match.competition.id != null
          })
          this.matches = matches
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getAccount  () {
      if (this.logged) {
        const path = 'http://' + this.host + '/account'
        axios.get(path, {
          headers: {
            Authorization: 'Bearer ' + this.token
          }
        }).then((res) => {
          if (this.matches_added.length === 0) {
            this.money_available = res.data.available_money
          }
          this.total_money = res.data.available_money
          this.is_admin = res.data.is_admin
        })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error)
            alert('Not Login')
            this.logOut()
          })
      }
    },
    finalizePurchase () {
      for (let i = 0; i < this.matches_added.length; i += 1) {
        const parameters = {
          match_id: this.matches_added[i].id,
          tickets_bought: this.matches_added[i].quantity
        }
        console.log(this.matches_added[i])
        if (parameters.tickets_bought > 0) {
          this.addPurchase(parameters)
        }
      }
      this.getMatches()
      this.getOrders()
      this.matches_added = []
    },
    addPurchase (parameters) {
      const path = `http://` + this.host + `/orders/${this.username}`
      axios.post(path, parameters, {
        headers: {
          Authorization: 'Bearer ' + this.token
        }})
        .then(() => {
          console.log('Order done')
          this.getAccount()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.getMatches()
        })
    },
    created () {
      this.getMatches()
    },
    addEventToCart (match) {
      if (match.total_available_tickets > 0) {
        if (match.quantity == null) {
          this.$set(match, 'quantity', 1)
          this.matches_added.push(match)
          this.money_available -= match.price
        } else {
          if (match.total_available_tickets - match.quantity - 1 >= 0) {
            this.$set(match, 'quantity', match.quantity + 1)
            this.money_available -= match.price
          }
        }
      }
    },
    purchase () {
      return this.matches_added.length === 0
    },
    buy (match) {
      if (match.quantity != null) {
        return this.money_available < match.price || (match.total_available_tickets - match.quantity - 1 < 0)
      }
      return this.money_available < match.price || (match.total_available_tickets - 1 < 0)
    },
    subEventToCart (match) {
      if (match.quantity > 0) {
        this.$set(match, 'quantity', match.quantity - 1)
        this.money_available += match.price
      }
    },
    removeEventToCart (match) {
      this.money_available += match.price * match.quantity
      const index = this.matches_added.indexOf(match)
      this.matches_added.splice(index, 1)
      match.quantity = null
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
  background-color: black;
}
.contendor {
  display: flex;
  align-items: center;
  justify-content: center;
}
.margen {
  margin-left: 10px;
}
.notificacion {
  margin-left: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #0d6efd;
  border-radius: 3px;
  color: white;
  width: 20px;
  height: 20px;
}
</style>
