<template>
    <el-card class="box-cards">
        <el-row :gutter="10">
            <el-col :span="8">
            <div class="podstyle">
                <h4>ServiceAccount</h4>
                <el-select v-model="serviceAccount" placeholder="请选择" style="width:80%;margin:5px" > 
                    <el-option
                    v-for="item in serviceOptions"
                    :key="item.value"
                    :value="item.value">
                    </el-option>
                </el-select>
                <h4>容器组重启策略</h4>
                <el-select v-model="restartPolicy" placeholder="请选择" style="width:80%;margin:5px"> 
                    <el-option
                    v-for="item in startOptions"
                    :key="item.value"
                    :value="item.value">
                    </el-option>
                </el-select>
            </div>
            </el-col>
            <el-col :span="12">
                <div  class="text item containerstyle">
                <el-form :model="podForm" :rules="rules" ref="podForm" label-width="100px" class="formelement">
                    <el-form-item label="容器名称" prop="name" >
                        <el-input v-model="podForm.name" placeholder="请输入容器名称"></el-input>
                    </el-form-item>
                    <el-form-item label="镜像" prop="image">
                        <el-input v-model="podForm.image" placeholder="请输入镜像"></el-input>
                    </el-form-item>
                    <el-form-item label="抓取策略" prop="imagePullPolicy">
                        <el-select v-model="podForm.imagePullPolicy" placeholder="请选择"> 
                            <el-option
                            v-for="item in graspPolicy"
                            :key="item.value"
                            :value="item.value"
                            >
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="工作目录" prop="workingDir">
                        <el-input v-model="podForm.workingDir" placeholder="请输入工作目录"></el-input>
                    </el-form-item>
                    <el-form-item label="Command" prop="command">
                         <div v-for="(item,index) in podForm.command" :key=index>
                            <div style="margin-bottom:5px">
                            <el-input v-model="podForm.command[index]" placeholder="command" style="width:200px;"></el-input>
                            <el-button type="text" style="padding-left:10px;"  @click="commandDelete(index)" >删除</el-button>
                            </div>
                        </div>
                        <el-button type="primary" plain size="small" @click="commandAdd">添加</el-button>
                    </el-form-item>
                    <el-form-item label="Args" prop="args">
                        <div v-for="(item,index) in podForm.args" :key=index>
                            <div style="margin-bottom:5px">
                            <el-input v-model="podForm.args[index]" placeholder="argument" style="width:200px;"></el-input>
                            <el-button type="text" style="padding-left:10px;"  @click="argsDelete(index)" >删除</el-button>
                            </div>
                        </div>
                        <el-button type="primary" plain size="small" @click="argsAdd">添加</el-button>
                    </el-form-item>
                    <el-form-item label="Ports" prop="ports">
                       <div v-for="(item,index) in podForm.ports" :key=index>
                            <div style="margin-bottom:5px">
                            <el-row :gutter="10" style="margin-left:10px">
                                <el-col :span="10">
                                    <el-input v-model="item.name" placeholder="name"></el-input>
                                </el-col>
                                <el-col :span="10">
                                    <el-select v-model="item.protocol" placeholder="请选择协议"  > 
                                        <el-option
                                            v-for="item in []"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                        </el-option>
                                    </el-select>
                                </el-col>
                            </el-row>
                            <el-row :gutter="10" style="margin-left:10px">
                                <el-col :span="10">
                                    <el-input v-model="item.containerPort" placeholder="ContainerPort" ></el-input>
                                </el-col>
                                <el-col :span="10">
                                    <el-input v-model="item.hostPort" placeholder="hostPort" ></el-input>
                                </el-col>
                                <el-col :span="2">
                                    <el-button type="text" style="padding-left:10px;"  @click="portsDelete(index)" >删除</el-button>
                                 </el-col>
                            </el-row>
                        
                            </div>
                        </div>
                        <el-button type="primary" plain size="small" @click="portsAdd">添加</el-button>
                    </el-form-item>
                    <el-form-item label="环境变量">
                        <div v-for="(item,index) in podForm.env" :key=index>
                            <div style="margin-bottom:5px">
                            <el-row :gutter="10" style="margin-left:10px">
                                <el-col :span="10">
                                    <el-input v-model="item.name" placeholder="变量名" ></el-input>
                                </el-col>
                                <el-col :span="10">
                                    <el-input v-model="item.value" placeholder="值" ></el-input>
                                </el-col>
                                <el-col :span="2">
                                    <el-button type="text" style="padding-left:10px;"  @click="envirDelete(index)" >删除</el-button>
                                 </el-col>
                            </el-row>
                            </div>
                        </div>
                         <div v-for="(item,index) in podForm.envFrom" :key=index>
                            <div style="margin-bottom:15px">
                                <el-select v-model="item.prefix" placeholder="将configMap导入环境变量"  > 
                                        <el-option
                                            v-for="item in []"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                        </el-option>
                                </el-select>
                                <el-button type="text" style="padding-left:10px;"  @click="configDelete(index)" >删除</el-button>
                            </div>
                        </div>
                        <el-button class="button-new-tag" size="small" @click="envirAdd">+ 名值对</el-button>
                        <el-button class="button-new-tag" size="small" @click="configAdd">+ 配置</el-button>
                    </el-form-item>
                    <el-form-item label="挂载点">
                        <div v-for="(item,index) in podForm.volumeMount" :key=index>
                            <div style="margin-bottom:5px">
                            <el-row :gutter="10" style="margin-left:10px">
                                <el-col>
                                    <el-input v-model="item.mountPath" placeholder="容器内目标路径"></el-input>
                                </el-col>
                            </el-row>
                            <el-row :gutter="10" style="margin-left:10px">
                                <el-col :span="10">
                                    <el-select v-model="item.readOnly" placeholder="请选择是否只读"  > 
                                        <el-option
                                            v-for="item in filemodes"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                        </el-option>
                                    </el-select>
                                </el-col>
                                <el-col :span="10">
                                    <el-select v-model="item.mountPropagation" placeholder="默认为none"  > 
                                        <el-option
                                            v-for="item in directions"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                        </el-option>
                                    </el-select>
                                </el-col>
                            </el-row>
                            <el-row :gutter="10" style="margin-left:10px">
                                <el-col :span="10">
                                    <el-select v-model="item.name" placeholder="数据卷"  > 
                                        <el-option
                                            v-for="item in []"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                        </el-option>
                                    </el-select>
                                </el-col>
                                <el-col :span="10">
                                      <el-input v-model="item.subPath_subPathExpr" placeholder="subPath/subPathExpr" ></el-input>
                                </el-col>
                            </el-row> 
                            <el-button type="text" style="padding-left:10px;"  @click="mountDelete(index)" >删除</el-button>
                            </div>
                        </div>
                        <el-button type="primary" plain size="small" @click="mountAdd">添加</el-button>
                    </el-form-item>
                     
                    <el-form-item label="CPU" v-show="sourceRestrict">
                        <el-row :gutter="5">
                            <el-col :span="10">
                                <el-input v-model="podForm.cpulimits.cpumin" placeholder="最小，如500m"></el-input>
                            </el-col>
                            <el-col :span="10">
                                <el-input v-model="podForm.cpulimits.cpumax" placeholder="最大，如1000m"></el-input>
                            </el-col>
                        </el-row>
                    </el-form-item>
                    <el-form-item label="内存" v-show="sourceRestrict">
                        <el-row :gutter="5">
                            <el-col :span="10">
                                <el-input v-model="podForm.memlimits.memmin" placeholder="最少，如200M"></el-input>
                            </el-col>
                            <el-col :span="10">
                                <el-input v-model="podForm.memlimits.memmax" placeholder="最大，如2G"></el-input>
                            </el-col>
                        </el-row>
                    </el-form-item>
                    <el-form-item>
                    <el-button type="primary" plain size="small" style="position:relative;left:-10px" v-show="!sourceRestrict" @click="sourceRestrict=true">资源限制</el-button>
                    </el-form-item>
                    <!--
                    <el-form-item>
                        <el-button type="primary" @click="submitForm('podForm')">立即创建</el-button>
                        <el-button @click="resetForm('podForm')">重置</el-button>
                    </el-form-item>
                    -->
                    </el-form>
                </div>
            </el-col>
        </el-row>
    </el-card>
</template>
<script>
import api from '@/api/api'
export default {
    data () {
        return {
            sourceRestrict:false,
            podForm:{
                name:'',
                image:'',
                imagePullPolicy:'',
                workingDir:'',
                command:[],
                args:[],
                ports:[],
                env:[],
                envFrom:[],
                volumeMount:[],
                cpulimits:{
                    cpumin:'',
                    cpumax:''
                }, 
                memlimits:{
                    memmin:'',
                    memmax:''
                },
            },
            serviceAccount:'',
            restartPolicy:'',
        
            commandCounter:0,
            argsCounter:0,
            portsCounter:0,
            envCounter:0,
            mountCounter:0,
            configCounter:0,

            serviceOptions:[{value:"default"}],
            startOptions:[{value:"Always"},{value:"Onfailure"},{value:"Never"}],
            graspPolicy:[{value:"always"},{value:"IfNotPresent"},{value:"Never"}],
            protocols:[{value:"TCP"},{value:"UDP"},{value:"SCTP"}],
            filemodes:[{value:"只读"},{value:"只写"}],
            directions:[{value:"none"},{value:"HosttoContainer"},{value:"Bidirectional"}],
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
                let form = this.podForm;
                 
                let types = "createpod"
                this.$emit("dataFromSub",types,form);

                /*
                api.addDeploymentTest(form).then(res => {
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
                */
                } else {
                console.log('error submit!!');
                return false;
                } 
            })
        },
        resetForm(formName) {
            this.$refs[formName].resetFields();
        },
        commandAdd() {
           this.podForm.command.push('');
        },
        commandDelete(index) {
            this.podForm.command.splice(index,1);
            
        },
        argsAdd() {
            this.podForm.args.push('');
        },
        argsDelete(index) {
            this.podForm.args.splice(index,1);
            
        },
        portsAdd() {
            this.podForm.ports.push( {
                        name:'',
                        protocol:'',
                        containerPort:'',
                        hostPort:'',
                    });
        },
        portsDelete(index) {
          this.podForm.ports.splice(index,1);
        },

        envirAdd() {
            this.podForm.env.push({
                name:'',
                value:''
            });
        },
        envirDelete(index) {
            this.podForm.env.splice(index,1);
        },
        configAdd() {
            this.posForm.envFrom.push({prefix:''});
        },
        configDelete(index) {
            this.podForm.envFrom.splice(index,1);
        },
        mountAdd() {
            this.podForm.volumeMount.push({
                mountPath:'',
                mountPropagation:'',
                name:'',
                readOnly:'',
                subPath_subPathExpr:''
            })
        },
        mountDelete(index) {
            this.podForm.volumeMount.splice(index,1);
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
    .box-cards {
    margin-left:10px;
    margin-right:10px;
    margin-top:10px;
    }
.podstyle{
    padding: 3px;
    border-width: 0px;
    border-radius:5px;
    border-style:solid;
    border-color:grey;
    margin:10px;
    background-color: #F8F8F8;
}
.containerstyle{
    padding: 3px;
    border-width: 1px;
    border-radius:5px;
    border-style:solid;
    border-color: #F8F8F8;
    margin:10px;
}
.formelement{
    width:80%;
    margin:5px;
}
</style>