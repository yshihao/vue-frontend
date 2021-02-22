<template>
    <div>
        <div class="filter-container">
            <div class="letf-items" style="display: inline-block">
                <el-select v-model="selectValue" placeholder="请选择查询字段">
                    <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    >
                        <span style="float: left">{{ item.label }}</span>
                        <!--<span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span> -->
                    </el-option>
                </el-select>
                <el-input
                    placeholder="输入查询"
                    style="width: 200px;"
                    class="filter-item"
                    v-model="inputValue"
                    @keyup.enter.native="handleFilter"
                    @input="handlesearch"
                />
                <!--<el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handlesearch">查询</el-button>  	 -->
            </div>
            <div class="btn_box_wapper">
                <el-button
                    class="filter-item"
                    style="margin-left: 10px;"
                    type="primary"
                    icon="el-icon-edit"
                    @click="handleCreate"
                >
                    伸缩
                </el-button>
                <el-button
                    class="filter-item"
                    style="margin-left: 10px;"
                    type="primary"
                    icon="el-icon-delete"
                >
                    YAML
                </el-button>
                <el-button
                    class="filter-item"
                    style="margin-left: 10px;"
                    type="primary"
                    icon="el-icon-arrow-right"
                    @click="$router.push({ path: '/home/createdeploy' })"
                >
                    创建 Deployment
                </el-button>
            </div>
        </div>
        <div style="top:10px;position:relative">
            <el-table
                :header-cell-style="{ background: '#eef1f6', color: '#606266' }"
                :data="tmpData"
                border="true"
                max-height="500"
                max-width="250"
                style="width: 100%"
            >
                <el-table-column label="Name" prop="name"></el-table-column>
                <el-table-column label="Ready" prop="ready"></el-table-column>
                <el-table-column
                    label="Up to Date"
                    prop="uptodate"
                ></el-table-column>
                <el-table-column
                    label="Available"
                    prop="available"
                ></el-table-column>

                <el-table-column label="Age" prop="age"></el-table-column>
                <el-table-column
                    align="right"
                    label="操作"
                    fixed="right"
                    width="350px"
                >
                    <template slot-scope="scope">
                        <el-button-group>
                            <el-button
                                icon="el-icon-edit"
                                size="mini"
                                @click="handleEdit(scope.$index, scope.row)"
                            >
                                查看
                            </el-button>
                            <el-button
                                size="mini"
                                icon="el-icon-thumb"
                                @click="handleEdit(scope.$index, scope.row)"
                            >
                                重启
                            </el-button>
                            <el-button
                                size="mini"
                                icon="el-icon-document"
                                @click="handleEdit(scope.$index, scope.row)"
                            >
                                Yaml
                            </el-button>
                            <el-button
                                size="mini"
                                icon="el-icon-delete"
                                type="danger"
                                @click="handleDelete(scope.$index, scope.row)"
                            >
                                删除
                            </el-button>
                        </el-button-group>
                    </template>
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>
<script>
import api from '@/api/api';
export default {
    data() {
        return {
            tableData: [],
            tmpData: [],
            options: [
                {
                    value: 1,
                    label: 'Name'
                },
                {
                    value: 2,
                    label: 'Ready'
                },
                {
                    value: 3,
                    label: 'Up to Date'
                },
                {
                    value: 4,
                    label: 'Available'
                },
                {
                    value: 5,
                    label: 'Age'
                }
            ],
            selectValue: '',
            inputValue: ''
        };
    },
    methods: {
        handleEdit(index, row) {
            console.log(index, row);
        },
        handlesearch() {
            if (this.selectValue == '') {
                this.inputValue = '';
                alert('请选择查询字段');
                return;
            }
            if (this.inputValue == '') {
                this.tmpData = this.tableData;
                return;
            }
            this.tmpData = [];
            switch (this.selectValue) {
                case 1:
                    this.tableData.filter(item => {
                        if (item.name.includes(this.inputValue)) {
                            this.tmpData.push(item);
                        }
                    });
                    break;
                case 2:
                    this.tableData.filter(item => {
                        if (item.ready.includes(this.inputValue)) {
                            this.tmpData.push(item);
                        }
                    });
                    break;
                case 3:
                    this.tableData.filter(item => {
                        if (item.uptodate.includes(this.inputValue)) {
                            this.tmpData.push(item);
                        }
                    });
                    break;
                case 4:
                    this.tableData.filter(item => {
                        if (item.available.includes(this.inputValue)) {
                            this.tmpData.push(item);
                        }
                    });
                    break;
                default:
                    this.tableData.filter(item => {
                        if (item.age.includes(this.inputValue)) {
                            this.tmpData.push(item);
                        }
                    });
            }
        },
        handleDelete(index, row) {
            console.log(index, row);
        },
        onSubmit() {},
        handleCreate() {}
    },
    mounted() {
        api.getDeploymentList()
            .then(res => {
                this.tableData = res.data.data;
                this.tmpData = res.data.data;
            })
            .catch(err => {
                console.log(err.response.status);
                /*if(err.response.status==401) {
          this.$store.commit('del_token')
          //this.$router.push({path:'/login'})
        }*/
                //
            });
    }
};
</script>

<style lang="less">
.filter-container {
    position: relative;
}

.btn_box_wapper {
    display: inline-block;
    position: absolute;
    right: 0;
}
</style>
