<template>
   <div class="container">
    <div class="row">
      <div class="col-sm-10">

    <h1>Cliente de las predicciones</h1>
     
    <b-form @submit="onSubmit" @reset="onReset" class="w-100">
    <b-form-group id="form-title-group"
                    label="glucosa:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="number"
                        v-model="d.var1"
                        required
                        placeholder="Enter glucosa">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                      label="insulina:"
                      label-for="form-author-input">
            <b-form-input id="form-author-input"
                          type="number"
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

      <alert :message=message v-if="showMessage"></alert>
    <div> 
      <hr>
      <p v-if="predictions != ''"> 
        Features:<b> {{features}}</b><br>
        Predict: <b>{{predictions}}</b>
        </p>
      <p v-else>No predicts!</p>          
    </div>

    </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  name: 'Predict',
  data: function() {
    return {
      features: "",
      predictions: "",
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

    predicter: function(payload) {
      const path = 'http://localhost:5001/api/predict';
      console.log(payload);
      axios.post(path, payload)
        .then((res) => {
          this.features = res.data.features;
          this.predictions = res.data.predictions;

          this.message = 'predict process ';
          this.showMessage = true;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    onSubmit: function(evt) {
      evt.preventDefault();
      const payload = {
        glucosa: this.d.var1,
        insulina: this.d.var2,
      };
      this.predicter(payload);
      this.initForm();
    },
    onReset: function(evt) {
      evt.preventDefault();
      this.initForm();
    },
    initForm: function() {
      this.d.var1 = '';
      this.d.var2 = '';

    },

  },

  created: function() {
  }

}
</script>
