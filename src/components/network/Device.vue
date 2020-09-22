<template>
    <div>
        <el-row>
          <el-col :span="24"><div style="text-align:center">device信息</div></el-col>
        </el-row>
        <el-row>
  
          <el-col :span="12"><div >
            <td>输入姓名：</td>
            <td>
                <el-input
            placeholder="无内容"
            v-model="input"
            :disabled="true">
          </el-input>
            </td>
          </div>
          </el-col>
        <el-col :span="12"><div >
             <td>输入姓名：</td>
            <td>
                <el-input
            placeholder="无内容"
            v-model="name"
            :disabled="true">
          </el-input>
            </td>
          </div></el-col>
        </el-row>
    </div>
</template>

<script>

export default{
    name: 'Ddvice',
    data() { 
        return {
        
            name:'this is me',
    
        }
      
    }


};

</script>

<style scoped>
.dockValue {
    background-color:cyan
    
}
 .el-row {
    margin-bottom: 20px;
  }
  .el-col {
    border-radius: 4px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
.form
{

     margin:0px;display: inline

}
</style>