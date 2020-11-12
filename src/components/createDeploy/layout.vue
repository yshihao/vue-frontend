<template>
      <div class="text item">
        <baseinfo></baseinfo>
        <br/>
        <createpod></createpod>
      </div>
</template>

<script>
import baseinfo from './baseinfo'
import createpod from './Createpod'
export default {
    data() {
        return {
        }
    },
    components:{
        baseinfo,
        createpod
    }
}
</script>

<style scoped>
.text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .box-card {
    width: 95%;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
    position: relative;
    left:2.5%;
    top:8px;

  }
</style>