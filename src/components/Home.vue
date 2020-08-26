<template>
    <div>
        <el-container style="height: 700px; border: 1px solid #eee">
        <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
            <el-menu :default-openeds="['1', '3']">
            <el-submenu index="1">
                <template slot="title"><i class="el-icon-message"></i>管理结点</template>
                <el-menu-item-group>
                <el-menu-item index="1-1" @click="add">新增结点</el-menu-item>
               
                <el-menu-item index="1-2" @click="add2">增加边</el-menu-item> 
                <el-menu-item index="1-3">删除结点</el-menu-item>
                <el-menu-item index="1-4">删除边</el-menu-item>
                </el-menu-item-group>
                
        
            </el-submenu>
            <el-submenu index="2">
                <template slot="title"><i class="el-icon-menu"></i>docker结点</template>
                <el-menu-item-group>
                
                <el-menu-item index="2-1">查看</el-menu-item>
                <el-menu-item index="2-2">查询</el-menu-item>
                </el-menu-item-group>
            </el-submenu>
            <el-submenu index="3">
                <template slot="title"><i class="el-icon-setting"></i>关于我们</template>
                <el-menu-item-group>
                <el-menu-item index="3-1">我们</el-menu-item>
                <el-menu-item index="3-2">联系我们</el-menu-item>
                </el-menu-item-group>
            </el-submenu>
            </el-menu>
        </el-aside>
        
        <el-container>
            <el-header style="text-align: right; font-size: 20px">
              <el-page-header @back="goBack" content="详情页面" v-if="flag==true">
              </el-page-header>
              <el-page-header @back="goBack2" content="详情页面" v-else-if="flag2==true">
              </el-page-header>
            </el-header>
            
            <el-main class="mainstyle"> 
            
            <div v-if="flag==true">
              <el-row>
              <el-button type="primary" round>增加结点</el-button>
              <el-button type="primary" round @click="ale('你已经提交增加结点请求')">提交</el-button>
              </el-row>
              <br/>
              <el-card class="box-card">
              <div slot="header" class="clearfix">
              <span>结点图</span>
              </div>
           
            </el-card> 
            </div>
            <div v-if="flag2==true">
              <el-row>
              <el-select v-model="value" placeholder="请选择结点1">
                <el-option>
                </el-option>
              </el-select>
              <el-select v-model="value" placeholder="请选择结点2">
                <el-option
                  v-for="item in options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
              <el-button type="primary" round @click="ale('你已经提交增加边请求')">提交</el-button>
              </el-row>
            </div>
            </el-main>
        </el-container>
        </el-container>

    </div>
</template>

<script>
export default {
  data:function(){
    return {
      flag:false,
      flag2:false
    }
    
  },
  methods:{
    add(){
    this.flag = !this.flag
    this.flag2 = false
    },
    goBack() {
      this.flag = !this.flag
        console.log('go back');
    },
     goBack2() {
      this.flag2 = !this.flag2
        console.log('go back');
    },
    add2(){
    this.flag2 = !this.flag2
    this.flag = false
    },
    ale(v) {
      alert(v)
    }
  }
    
}
</script>

<style scoped>
.el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 60px;
  }
  
  .el-aside {
    color: #333;
  }
   .text {
    font-size: 14px;
  }
  .mainstyle{
    color: black;

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
    width: 1300px;
    height: 700px;

  }
</style>