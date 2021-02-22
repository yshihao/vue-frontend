<template>
    <el-card class="box-cards1">
        <div slot="header" class="clearfix">
            <span>基本信息</span>
            <el-button style="float: right; padding: 3px 0" type="text">
                操作按钮
            </el-button>
        </div>
        <div class="text item">
            <el-form
                :model="serviceForm"
                :rules="rules"
                ref="serviceForm"
                label-width="100px"
                class="demo-ruleForm"
            >
                <el-form-item label="服务类型" prop="kind">
                    <el-select
                        v-model="serviceForm.kind"
                        placeholder="请选择服务类型"
                    >
                        <el-option
                            v-for="(items, index) in options"
                            :key="index"
                            :value="items.value"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <!--
            <el-form-item label="服务分层" prop="layer">
                <el-select v-model="serviceForm.layer" placeholder="请选择服务分层">
                <el-option label="区域一" value="shanghai"></el-option>
                <el-option label="区域二" value="beijing"></el-option>
                </el-select>
            </el-form-item>
            -->
                <el-form-item label="服务名称" prop="name">
                    <el-input v-model="serviceForm.name"></el-input>
                </el-form-item>
                <el-form-item label="注解" prop="annotations">
                    <el-dialog :visible.sync="commentFormVisible">
                        <el-form :model="tagform">
                            <el-form-item
                                label="注解名"
                                :label-width="formLabelWidth"
                            >
                                <el-input
                                    v-model="tagform.key"
                                    autocomplete="off"
                                ></el-input>
                            </el-form-item>
                            <el-form-item
                                label="注解值"
                                :label-width="formLabelWidth"
                            >
                                <el-input
                                    v-model="tagform.value"
                                    autocomplete="off"
                                ></el-input>
                            </el-form-item>
                        </el-form>
                        <div slot="footer" class="dialog-footer">
                            <el-button @click="commentFormVisible = false">
                                取 消
                            </el-button>
                            <el-button
                                type="primary"
                                @click="handlecommentConfirm"
                            >
                                确 定
                            </el-button>
                        </div>
                    </el-dialog>
                    <el-tag
                        v-for="(item, index) in serviceForm.annotations"
                        :key="index"
                        closable
                        @close="handclosecomment(item)"
                    >
                        {{ Object.keys(item)[0] }}:{{
                            item[Object.keys(item)[0]]
                        }}
                    </el-tag>
                    <el-button
                        class="button-new-tag"
                        size="small"
                        @click="showcomment"
                    >
                        + New Tag
                    </el-button>
                </el-form-item>
                <el-form-item label="标签" prop="labels">
                    <el-dialog :visible.sync="tagFormVisible">
                        <el-form :model="tagform">
                            <el-form-item
                                label="标签名"
                                :label-width="formLabelWidth"
                            >
                                <el-input
                                    v-model="tagform.key"
                                    autocomplete="off"
                                ></el-input>
                            </el-form-item>
                            <el-form-item
                                label="标签值"
                                :label-width="formLabelWidth"
                            >
                                <el-input
                                    v-model="tagform.value"
                                    autocomplete="off"
                                ></el-input>
                            </el-form-item>
                        </el-form>
                        <div slot="footer" class="dialog-footer">
                            <el-button @click="tagFormVisible = false">
                                取 消
                            </el-button>
                            <el-button type="primary" @click="handletagConfirm">
                                确 定
                            </el-button>
                        </div>
                    </el-dialog>
                    <el-tag
                        v-for="(item, index) in serviceForm.labels"
                        :key="index"
                        closable
                        @close="handclosetag(item)"
                    >
                        {{ Object.keys(item)[0] }}:{{
                            item[Object.keys(item)[0]]
                        }}
                    </el-tag>
                    <el-button
                        class="button-new-tag"
                        size="small"
                        @click="showtag"
                    >
                        + New Tag
                    </el-button>
                </el-form-item>
                <el-form-item label="副本数量" prop="replicas">
                    <el-input-number
                        v-model="serviceForm.replicas"
                        @change="handlenumChange(serviceForm.replicas)"
                        :max="100"
                        label="描述文字"
                    ></el-input-number>
                </el-form-item>

                <el-form-item>
                    <el-button
                        type="primary"
                        @click="submitForm('serviceForm')"
                    >
                        立即创建
                    </el-button>
                    <el-button @click="resetForm('serviceForm')">
                        重置
                    </el-button>
                </el-form-item>
            </el-form>
        </div>
    </el-card>
</template>
<script>
import api from '@/api/api';
export default {
    data() {
        return {
            formLabelWidth: '',
            tagFormVisible: false,
            commentFormVisible: false,
            tags: [],
            comments: [],
            options: [
                {
                    value: 'StatefulSet'
                },
                {
                    value: 'Deployment'
                },
                {
                    value: 'DaemonSet'
                }
            ],

            tagform: {
                key: '',
                value: ''
            },
            serviceForm: {
                kind: '',
                name: '',
                annotations: [],
                labels: [],
                replicas: 0
            },
            rules: {
                kind: [
                    {
                        required: true,
                        message: '请选择服务类型',
                        trigger: 'blur'
                    }
                ],
                name: [
                    {
                        required: true,
                        message: '请输入服务名称',
                        trigger: 'blur'
                    },
                    {
                        min: 3,
                        max: 20,
                        message: '长度在 3 到 20 个字符',
                        trigger: 'blur'
                    }
                ],
                labels: [
                    { required: true, message: '请选择标签', trigger: 'blur' }
                ],
                replicas: [
                    {
                        required: true,
                        message: '请选择副本数量',
                        trigger: 'blur'
                    }
                ]
            }
        };
    },
    methods: {
        submitForm(formName) {
            this.$refs[formName].validate(valid => {
                if (valid) {
                    let form = this.serviceForm;
                    let types = 'baseinfo';
                    this.$emit('dataFromSub', types, form);
                    //console.log("send data");
                    /*
            api.addDeploymentTest(form).then(res=>{
                let mystate = res.data.code;
                console.log(mystate);
                if(mystate== 200) {
                   alert('submit!');
                }
            }).catch(err=>{
                console.log(err);
            })*/
                } else {
                    console.log('error submit!!');
                    return false;
                }
            });
        },
        resetForm(formName) {
            this.$refs[formName].resetFields();
        },
        showtag() {
            this.tagFormVisible = true;
            /* this.$nextTick(_ => {
          this.$refs.saveTagInput.$refs.input.focus();
        });*/
        },
        showcomment() {
            this.commentFormVisible = true;
        },
        handletagConfirm() {
            this.tagFormVisible = false;
            let key = this.tagform.key;
            let value = this.tagform.value;
            if (key && value) {
                //this.serviceForm.tag[key]=value;
                this.serviceForm.labels.push({ key: value });
                this.tagform.key = '';
                this.tagform.value = '';
            }
        },
        handclosetag(key) {
            //console.log(key);
            //this.$delete(this.serviceForm.tag,key);
            //delete this.serviceForm.tag[key];
            this.serviceForm.labels.splice(
                this.serviceForm.labels.indexOf(key),
                1
            );
        },
        handclosecomment(key) {
            // this.$delete(this.serviceForm.comment,key);
            this.serviceForm.annotations.splice(
                this.serviceForm.comment.indexOf(key),
                1
            );
        },
        handlecommentConfirm() {
            this.commentFormVisible = false;
            let key = this.tagform.key;
            let value = this.tagform.value;
            if (key && value) {
                // this.serviceForm.comment.push({key:name,value:value});
                this.serviceForm.annotation.push({ key: value });
                this.tagform.key = '';
                this.tagform.value = '';
            }
        },
        handlenumChange(v) {
            console.log(v);
        }
    }
};
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
    content: '';
}
.clearfix:after {
    clear: both;
}
.box-cards1 {
    margin-left: 10px;
    margin-top: 10px;
}
</style>
