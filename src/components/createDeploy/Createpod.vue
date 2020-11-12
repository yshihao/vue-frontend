<template>
    <el-card class="box-card">
        <div  class="text item">
            <el-form :model="podForm" :rules="rules" ref="podForm" label-width="100px" class="demo-ruleForm">
            <el-form-item label="容器名称" prop="Containername">
                <el-input v-model="podForm.Containername" ></el-input>
            </el-form-item>
            <el-form-item label="镜像" prop="Imagename">
                <el-input v-model="podForm.Imagename" ></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('podForm')">立即创建</el-button>
                <el-button @click="resetForm('podForm')">重置</el-button>
            </el-form-item>
            </el-form>
        </div>
    </el-card>
</template>
<script>
import api from '@/api/api'
export default {
    data () {
        return {
            podForm:{
                Containername:'',
                Imagename:''
            },
            rules:{
            Containername: [
              {required:true,message:'请输入容器名称',trigger:'blur'}
            ],
            Imagename: [
              {required:true,message:'请输入镜像',trigger:'blur'}
            ]
            },
        };   
    },
    
    methods: {
        submitForm(formname) {
            this.$refs[formname].validate((valid) =>{
                if (valid) {
                
                let name = this.podForm.Containername;
                let imagename = this.podForm.Imagename;
                api.addContainer(name,imagename).then(res => {
                    let mystate = res.data.code;
                    if(mystate==200) {
                        alert('添加成功');
                    }else{
                        alert('添加失败!')
                    }
                    console.log(mystate)
                }).catch(err=>{
                    console.log(err);
                })

                } else {
                console.log('error submit!!');
                return false;
                } 
            })
        },
        resetForm(formName) {
            this.$refs[formName].resetFields();
        },
    },
}
</script>
<style>
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