<template>
    <el-card class="box-card">
        <div slot="header" class="clearfix">
            <span>Deployment列表</span>
            
        </div>
        <div class="text item">
            <Table></Table>
        </div>
    </el-card>

</template>

<script>
import Table from './Tablepod'
export default {
    data() {
        return {
        }
    },
    components:{
        Table
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