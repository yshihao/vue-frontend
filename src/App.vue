
<template>
    <div id="app">
      <Home></Home>
    </div>
</template>

<script>


import Home from  './components/Home.vue'
export default {
    name: "App",
    data: function(){
      return {
      }
    },
    methods:{
     
    },
    components: {
     Home:Home
    }
}
</script>

<style scoped>
p{
  background:red;
}
button{
  background:white;
}

*{
  margin: 0%;
  padding: 0%;
}
.size{
  font-size: 100px;
}
.color{
  color: red;
}
.active{
  background:yellow;
}

</style>