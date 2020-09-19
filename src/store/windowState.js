const state = () => ({
    windowHeight: document.documentElement.clientHeight,
    windowWidth: document.documentElement.windowWidth
});

const getters = {
    graphHeight(state) {
        return state.windowHeight - 201;
    },
    graphWidth(state) {
        return state.windowWidth - 315;
    }
};

const mutations = {
    updateHeight(state, height) {
        // console.log(height);
        state.windowHeight = height;
    },
    updateWidth(state, width) {
        // console.log(width);
        state.windowWidth = width;
    }
};

export default {
    namespcaed: true,
    state,
    getters,
    mutations
};
