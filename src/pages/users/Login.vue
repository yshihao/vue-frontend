<template>
    <div class="login-container">
        <el-form
            :model="loginForm"
            :rules="rules"
            ref="loginForm"
            label-position="left"
            label-width="0px"
        >
            <h3 class="title">Welcome_to_Login</h3>
            <el-form-item prop="email">
                <el-input
                    type="text"
                    v-model="loginForm.email"
                    auto-complete="off"
                    placeholder="m.Email"
                    @keyup.enter.native="handleLogin"
                ></el-input>
            </el-form-item>
            <el-form-item prop="password">
                <el-input
                    type="password"
                    v-model="loginForm.password"
                    auto-complete="off"
                    placeholder="m.Password"
                    @keyup.enter.native="handleLogin"
                ></el-input>
            </el-form-item>
            <el-form-item style="width:100%;">
                <el-button
                    type="primary"
                    style="width:100%;"
                    @click.native.prevent="handleLogin"
                    :loading="logining"
                >
                    登陆
                </el-button>
            </el-form-item>
            <el-form-item style="width:100%;">
                <el-button
                    type="primary"
                    style="width:100%;"
                    @click.native.prevent="handleToRegister"
                >
                    注册
                </el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
export default {
    name: 'login',
    data() {
        let checkPassword = (rule, value, callback) => {
            if (value.length < 6 || value.length > 16) {
                callback(new Error('Password_Length_Error'));
            } else {
                callback();
            }
        };
        let checkEmail = (rule, value, callback) => {
            const mailReg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
            if (mailReg.test(value)) {
                callback();
            } else {
                callback(new Error('Email_Format_Error'));
            }
        };
        return {
            logining: false,
            loginForm: {
                email: '',
                password: ''
            },

            rules: {
                email: [
                    { required: true, trigger: 'blur'}
                ],
                password: [
                    {
                        required: true,
                        trigger: 'blur',
                    }
                ]
            }
        };
    },
    methods: {
        handleRoute(route) {
            
            // TODO 根据用户身份选择跳转到不同的页面
        },
        handleLogin() {
            sessionStorage.setItem("flag", 1);
            this.$router.push({path:"/home"})
            alert("登陆成功")
            
        },
        handleToRegister() {
            this.$router.push({path:"/register"})
        }
    }
    // beforeRouteLeave(to, from, next){
    //   if(to.name ==='item' && ( this.isActive===false || this.isActive === undefined)){
    //     this.$router.push('/activate')
    //   }
    //   else
    //   {
    //     next()
    //   }
    //}
};
</script>

<style lang="less" scoped>
.login-container {
    position: relative;
    -webkit-border-radius: 5px;
    border-radius: 5px;
    -moz-border-radius: 5px;
    background-clip: padding-box;
    top: 100px;
    margin: auto;
    width: 350px;
    padding: 35px 35px 15px 35px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;
    .title {
        margin: 0px auto 20px auto;
        text-align: center;
        color: #505458;
    }
}
</style>
