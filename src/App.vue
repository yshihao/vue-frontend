<template>
    <div id="app">
        <Home></Home>
    </div>
</template>

<script>
import Home from './components/Home.vue';
import { mapMutations } from 'vuex';

export default {
    name: 'App',
    data: function() {
        return {};
    },
    methods: {
        ...mapMutations(['updateHeight', 'updateWeight'])
    },
    components: {
        Home: Home
    },
    mounted() {
        window.onresize = () => {
            this.$store.commit(
                'updateHeight',
                document.documentElement.clientHeight
            );
            this.$store.commit(
                'updateWidth',
                document.documentElement.clientWidth
            );
        };
    }
};
</script>

<style scoped>
/* p {
    background: red;
}
button {
    background: white;
}

* {
    margin: 0%;
    padding: 0%;
}
.size {
    font-size: 100px;
}
.color {
    color: red;
}
.active {
    background: yellow;
} */
</style>
