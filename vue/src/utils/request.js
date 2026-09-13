import { ElMessage } from 'element-plus'
import router from '../router'
import axios from "axios";

const request = axios.create({
    baseURL: import.meta.env.VITE_BASE_URL,
    timeout: 30000  // 后台接口超时时间设置
})

// request 拦截器
request.interceptors.request.use(config => {
    if (!(config.data instanceof FormData)) {
        config.headers['Content-Type'] = 'application/json;charset=utf-8';
    }
    // 附加 JWT token
    const token = sessionStorage.getItem('access_token')
    if (token) {
        config.headers['Authorization'] = 'Bearer ' + token
    }
    return config
}, error => {
    return Promise.reject(error)
});

// response 拦截器
request.interceptors.response.use(
    response => {
        let res = response.data;
        // 如果是返回的文件
        if (response.config.responseType === 'blob') {
            return res
        }
        // 兼容服务端返回的字符串数据
        if (typeof res === 'string') {
            res = res ? JSON.parse(res) : res
        }
        // 当权限验证不通过的时候给出提示
        if (res.code === '401') {
            ElMessage.error(res.msg || '登录已过期，请重新登录');
            // 只在前台首页不跳转登录页，其他页面（包括登录页）都允许跳转
            const isFrontPage = router.currentRoute.value.path === '/'
            if (!isFrontPage) {
                router.push("/login")
            }
            sessionStorage.removeItem('access_token')
            sessionStorage.removeItem('system-user')
        }
        return res;
    },
    error => {
        // HTTP 401 错误处理（JWT 认证失败）
        if (error.response && error.response.status === 401) {
            const msg = error.response.data?.msg || '登录已过期，请重新登录'
            ElMessage.error(msg)
            sessionStorage.removeItem('access_token')
            sessionStorage.removeItem('system-user')
            // 只在前台首页不跳转登录页
            const isFrontPage = router.currentRoute.value.path === '/'
            if (!isFrontPage) {
                router.push("/login")
            }
        }
        return Promise.reject(error)
    }
)


export default request
