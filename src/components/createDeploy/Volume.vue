<template>
    <el-card>
        <div slot="header" class="clearfix">
            <span>数据卷</span>
        </div>
        <div class="text item" >
          <div v-for="(d,index) in counter" :key=index>
            <div style="margin-bottom:5px">
              <el-input v-model="input[index]" placeholder="请输入内容" style="width:200px;"></el-input>
              <el-select v-model="value[index]" placeholder="请选择" class="input-lay" @change="selected"> 
                  <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                  </el-option>
              </el-select>
              <el-button type="text" style="padding-left:10px;"  @click="deletec(index)" >删除</el-button>
            </div>
          </div>
          <el-button type="success" plain style="margin-top:10px;" :disabled="buttonVisit" @click="add">添加</el-button>
        </div>
        
    </el-card>
</template>
<script>
export default {
    name:'volume',
    data(){
      return {
        buttonVisit:false,
        input:[],
        value:[],
        options:[ {
          value: '选项1',
          label: '黄金糕'
        }, {
          value: '选项2',
          label: '双皮奶'
        }],
        counter:[],
      }
    },
    methods:{
      add() {
        this.buttonVisit = !this.buttonVisit;
        this.counter.push({});
      },
      deletec(index) {
        this.counter.splice(index,1);
        this.input.splice(index,1);
        this.value.splice(index,1);
        console.log(this.input.length);
        if(this.value.length==0&& this.input.length==0) {
          this.buttonVisit = false;
        }
        console.log(index);
      },
      selected() {
        this.buttonVisit = !this.buttonVisit;
        console.log(this.value);
      }
    }
}
</script>
<style >
  .text {
    font-size: 14px;
  }
  .item {
    margin-bottom: 18px;
  }
  .volume-cards{
    margin-right:10px;
    margin-top:10px;
    height:600px;
  }
  .input-lay{
    display:inline;
    width:40%;
    margin-left:10px;
  }
</style>