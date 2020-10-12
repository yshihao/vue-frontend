<template>
    <div>
        <el-row>
            <div style="text-align:center">
                <el-col>Device 详细信息</el-col>
                <br />
                <br />

                <div v-for="(value, name, index) in objects" v-bind:key="index">
                    <p>
                        <label>{{ name }}:</label>
                        <input type="text" :value="value" disabled="true" />
                        <br />
                    </p>
                </div>
            </div>
        </el-row>
    </div>
</template>
<script>
import api from '../../api/api';
export default {
    name: 'Ddvice',
    data() {
        return {
            objects: {}
        };
    },
    created() {
        this.id = this.$route.params.deviceName;
        console.log(this.id);
        api.getDockerDevice(this.$route.params.id).then(res => {
            this.objects = res.data.data;
        });
    }
};
</script>

<style scoped>
input {
    font-size: 24px;
    border: none;
    width: 10cm;
    background: white;
    text-align: center;
}
label {
    cursor: pointer;
    display: inline-block;
    padding: 3px 6px;
    text-align: right;
    width: 150px;
    vertical-align: top;
}
</style>
