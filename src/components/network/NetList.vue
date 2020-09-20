<template>
    <div>
        <div>test</div>
        <el-card
            shadow="hover"
            v-for="item in netList"
            :key="item"
            class="net-item"
        >
            {{ item }}
        </el-card>
    </div>
</template>

<script>
export default {
    name: 'NetList',
    props: ['netList']
};
</script>
