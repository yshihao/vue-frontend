<!-- 
  创建deploy需要 配置baseinfo、service、volume等  全部放在这个组件里布局
-->
<template>
      <div class="text item" >
        <div class="save"> 
            <span class="inmiddle">创建工作负载</span>
            <el-button type="info" size="small" @click="handleParentoff">取消</el-button>
            <el-button type="primary" size="small" @click="handleParent">保存</el-button>
        </div>
        <div style="display:block">
        <el-row :gutter="10">
          <el-col :span="12">
            <baseinfo class="volume-cards" ref="baseinfo" @dataFromSub="dataFromSubComponent(arguments)"></baseinfo>
          </el-col>
          <el-col :span="12">
             <volume class="volume-cards"></volume>
          </el-col>
          
        </el-row>
        <el-row>
        <createpod ref="createpod" @dataFromSub="dataFromSubComponent(arguments)"></createpod>
        </el-row>
        </div>
      </div>
</template>

<script>
import baseinfo from './baseinfo'
import createpod from './Createpod'
import volume from './Volume'
import service from './Service'
import api from '@/api/api'

export default {

    data() {
        return {
          deploy_infos:'',
          containers:'',
        }
    },
    methods:{
      handleParentoff() {
        this.$refs.baseinfo.resetForm("serviceForm");
        this.$refs.createpod.resetForm("podForm");
      },
      handleParent() {
        this.$refs.baseinfo.submitForm("serviceForm");
        this.$refs.createpod.submitForm("podForm");
        
        api.addDeployment(this.deploy_infos,this.containers).then(res =>{
            console.log(res.data.code);
        }).catch(err=>{
          console.log(err);
        });

      },
      dataFromSubComponent(data) {
        let types = data[0];
        //console.log(types);
        if(types=="baseinfo") {
          this.deploy_infos = data[1];
        }else if (types=="createpod") {
          this.containers = data[1];
        }
        //console.log(this.deploy_infos['name']);
      },
    },
    components:{
        baseinfo,
        createpod,
        volume,
    }
}
</script>

<style scoped>
.text {
    font-size: 14px;
    position:relative;
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
  .volume-cards{
    margin-right:10px;
    margin-top:10px;
  }
  .el-row{
    margin-bottom: 20px;
  }
  .save{
    border-width: 0px;
    border-radius:5px;
    border-style:solid;
    border-color:grey;
    margin:10px;
    background-color: #CCFFFF;
  
    z-index:100;  
    
  }
  .inmiddle {
    margin-left:40%;
    margin-right:10px;
  }
</style>