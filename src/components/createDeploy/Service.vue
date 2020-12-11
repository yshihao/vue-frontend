<template>
    <div>
        <el-row :gutter="10">
            <el-col :span="12">
                <el-card class="box-cards">
                    <div slot="header" class="clearfix">
                        <span>访问方式Service</span>
                    </div>
                    <div class="text item ">
                        <el-radio-group v-model="radio">
                            <el-radio :label="3">备选项</el-radio>
                            <el-radio :label="6">备选项</el-radio>
                            <el-radio :label="9">备选项</el-radio>
                        </el-radio-group>
                        <div class="podstyle" style="height:30%;">
                            <el-dialog  :visible.sync="commentFormVisible">
                                <el-form :model="tagform">
                                    <el-form-item label="注解名" :label-width="formLabelWidth">
                                    <el-input v-model="tagform.name" autocomplete="off"></el-input>
                                    </el-form-item>
                                    <el-form-item label="注解值" :label-width="formLabelWidth">
                                    <el-input v-model="tagform.value" autocomplete="off"></el-input>
                                    </el-form-item>
                                </el-form>
                                <div slot="footer" class="dialog-footer">
                                    <el-button @click="commentFormVisible = false">取 消</el-button>
                                    <el-button type="primary" @click="handlecommentConfirm">确 定</el-button>
                                </div>
                            </el-dialog>
                            <span>注解</span>
                            <el-tag
                            v-for="tag in comments"
                            :key="tag.name"
                            closable
                            :type="tag.type"
                            @close="handclosecomment(tag)">
                            {{tag.name}}:{{tag.value}}
                            </el-tag>
                            <el-button class="button-new-tag" size="small" @click="showcomment">+ 注解</el-button>
                            
                        </div>
                        <div class="podstyle" style="height:30%;">
                            <div>
                                <el-row :gutter="10">
                                    <el-col :span="4">
                                        <span>端口名称</span>
                                    </el-col>
                                    <el-col :span="4">
                                        <span>协议</span>
                                    </el-col>
                                    <el-col :span="4">
                                        <span>服务端口</span>
                                    </el-col>
                                    <el-col :span="4">
                                        <span>容器端口</span>
                                    </el-col>
                                    <el-col :span="4">
                                        <span>操作</span>
                                    </el-col>
                                </el-row>
                                <div v-for="index in serviceCounter" :key=index>
                                    <el-row :gutter="10">
                                        <el-col :span="4">
                                            <el-input v-model="serviceForm.portName[index]" placeholder="输入"></el-input>
                                        </el-col>
                                        <el-col :span="4">
                                            <el-select v-model="serviceForm.protocol[index]" placeholder="请选择"> 
                                                <el-option
                                                v-for="item in protocolList"
                                                :key="item.value"
                                                :value="item.value"
                                                >
                                                </el-option>
                                            </el-select>
                                        </el-col>
                                        <el-col :span="4">
                                           <el-input v-model="serviceForm.servicePort[index]" placeholder="输入"></el-input>
                                        </el-col>
                                        <el-col :span="4">
                                           <el-input v-model="serviceForm.containerPort[index]" placeholder="输入"></el-input>
                                        </el-col>
                                        <el-col :span="4">
                                            <el-button type="text" style="padding-left:10px;"  @click="serviceDelete(index)" >删除</el-button>
                                        </el-col>
                                    </el-row>
                                    
                                </div>
                                <el-button type="primary" plain size="small" @click="serviceAdd">添加</el-button>
                            </div>
                        </div>
                        <div class="podstyle" style="height:40%">
                           <el-form :model="sessionForm" :rules="rules" ref="sessionForm" label-width="100px">
                                <el-form-item label="sessionAffinity" prop="sessionaffinity">
                                    <el-select v-model="sessionForm.sessionaffinity" placeholder="请选择" @change="selectValue(sessionForm.sessionaffinity)"> 
                                        <el-option
                                        v-for="item in sessionPolicy"
                                        :key="item.value"
                                        :value="item.value"
                                        >
                                        </el-option>
                                    </el-select>
                                    <div v-show="timeoutshow==true">
                                        <span>timeoutseconds</span>
                                        <el-input v-model="timeoutseconds"  style="width:200px;"></el-input>
                                    </div>
                                    
                                </el-form-item>
                                <el-form-item label="externalIPs" prop="externalip">
                                    <div v-for="index in ipCounter" :key=index>
                                        <div style="margin-bottom:5px">
                                        <el-input v-model="sessionForm.externalip[index]"  style="width:200px;"></el-input>
                                        <el-button type="text" style="padding-left:10px;"  @click="ipDelete(index)" >删除</el-button>
                                        </div>
                                    </div>
                                    <el-button type="primary" plain size="small" @click="ipAdd">添加</el-button>
                                </el-form-item>
                           </el-form>
                        </div>
                    </div>
                </el-card>
                
            </el-col>

            <el-col :span="12">
                <el-card class="box-cards">
                    <div slot="header" class="clearfix">
                        <span>互联网入口Ingress</span>
                    </div>

                    <div class="text item"  style="margin:10px;height:300px;">
                        
                    </div>
                </el-card>
            </el-col>
            
            
        </el-row>
        
    </div>
    
</template>
<script>
import api from '@/api/api'
export default {
    data () {
        return {
            radio:'',
            serviceCounter:0,
            protocolList:[{value:"TCP"},{value:"UDP"}],
            ipCounter:0,
            commentFormVisible:false,
            timeoutshow:false,
            timeoutseconds:'',
            comments: [
            { name: '标签一',value:'dsf',type: '' },
            { name: '标签二', value:'dfsd',type: 'success' },
            ],
            tagform:{
             name:'',
             value:''
            },
            serviceForm:{
                portName:[],
                protocol:[],
                servicePort:[],
                containerPort:[]
            },
            sessionForm:{
                sessionaffinity:'',
                externalip:[],
            },
            sessionPolicy:[{value:'None'},{value:'clientIp'}]
        }
           
    },
    
    methods:{
       handclosecomment(tag) {
          this.comments.splice(this.comments.indexOf(tag),1);
        },
       showcomment() {
          this.commentFormVisible = true;
        },
      handlecommentConfirm() {
        this.commentFormVisible = false;
        let name = this.tagform.name;
        let value = this.tagform.value;
        if (name&&value) {
          this.comments.push({name:name,value:value});
          this.tagform.name="";
          this.tagform.value="";
        }
        
      },
      ipAdd() {
          this.ipCounter++;
      },
      ipDelete(index) {
          this.ipCounter--;
          this.sessionForm.externalip.splice(index,1);
      },
      serviceAdd(){
          this.serviceCounter++;
      },
      serviceDelete(index) {
          this.serviceCounter--;
          this.serviceForm.portName.splice(index,1);
          this.serviceForm.protocol.splice(index,1);
          this.serviceForm.servicePort.splice(index,1);
          this.serviceForm.containerPort.splice(index,1);

      },
      selectValue(value) {
          if(value=="clientIp") {
              this.timeoutshow = true;
          }else {
              this.timeoutshow = false;
          }
          console.log(value);
      }

    }
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