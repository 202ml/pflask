<template>
  <div class="hello">
    <h1>Cliente de las predicciones</h1>
    <alert :message=message v-if="showMessage"></alert>
    <p> 
      {{ resp }}
    </p> 
    <b-form @submit="onSubmit" @reset="onReset" class="w-100">
    <b-form-group id="form-title-group"
                    label="glucosa:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="d.var1"
                        required
                        placeholder="Enter glucosa">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                      label="insulina:"
                      label-for="form-author-input">
            <b-form-input id="form-author-input"
                          type="text"
                          v-model="d.var2"
                          required
                          placeholder="Enter insulina">
            </b-form-input>
          </b-form-group>
    
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>

    
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  name: 'Predict',
  data: function() {
    return {
      resp: "",
      d: {
        var1: '',
        var2: '',
      },
      message: '',
      showMessage: false,
    }
  },   
  components: {
    alert: Alert,
  },
  methods: {
    predecix: function() {
      const path = 'http://localhost:5001/api/predict';
      axios.get(path)
        .then((res) => {
          this.resp = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
        
    },
    addBook(payload) {
      const path = 'http://localhost:5001/api/predict';
      console.log(payload);
      axios.post(path, payload)
        .then((res) => {
          this.resp = res.data;

          
          this.message = 'predict process!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          //this.getBooks();
        });
    },
    onSubmit(evt) {
      evt.preventDefault();
      const payload = {
        glucosa: this.d.var1,
        insulina: this.d.var2,
      };
      this.addBook(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.initForm();
    },
    initForm() {
      this.d.var1 = '';
      this.d.var2 = '';

    },

  },

  created: function() {
    //this.predecir();
  }, 

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.hello {
color: #42b983;
}
</style>