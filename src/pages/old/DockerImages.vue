<template>
   <div class="divs">
       <div>
       <el-form :inline="true" :model="formInline" class="demo-form-inline">
            <el-form-item label="镜像列表">
                <el-select v-model="formInline.imageName" placeholder="选取镜像">
                <el-option v-for="item in imageList" :key="item.value" :label="item.label" :value="item.vlaue"></el-option>
                </el-select>
            </el-form-item>
        </el-form>
        <el-form :inline="true" :model="formInline" class="demo-form-inline">
            <el-form-item label="镜像名">
                <el-input v-model="formInline.user" placeholder="镜像名"></el-input>
            </el-form-item>
             <el-form-item label="镜像创建时间">
                <el-input v-model="formInline.user" placeholder="镜像创建时间"></el-input>
            </el-form-item>
            
        </el-form>
        <el-form :model="formInline" class="demo-form-inline">
            <el-form-item label="镜像地址" label-width="70px" >
                <el-input v-model="formInline.user" placeholder="镜像地址"></el-input>
            </el-form-item>        
        </el-form>
        <el-form>
            <el-form-item label="备注">
                <el-input type="textarea" placeholder="备注"></el-input>
            </el-form-item>
        </el-form>
        </div>
        <div>

        
            <el-button @click="drawer = true" type="primary" style="margin-left: 16px;">
                    点我打开
            </el-button>
        <el-drawer
            title="我是标题"
            :visible.sync="drawer"
            :direction="direction"
            :before-close="handleClose">
            <span>我来啦!</span>
        </el-drawer>
        </div>
   </div>
    
</template>

<script>
export default {
    name: 'DockerImages',
    data() {
        return {
            drawer:false,
            direction:'ltr',
            formInline:{
                user:'',
                imageName:''
            },
            imageList:[{
                value:'选项1',
                label:'image1'
            },{
                value:'选项2',
                label:'image2'
            },
            {
                value:'选项3',
                label:'image3'
            },]
        }
    }
};
</script>

<style scoped>
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
.divs{
    margin:20px auto;
    height:400px;
    position:absolute;
    top:20%;
    left: 40%;
   /* border: 4px solid floralwhite;*/
}
</style>


