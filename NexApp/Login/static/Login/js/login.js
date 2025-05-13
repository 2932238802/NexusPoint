//——————————————————————————————————————————————————————————————————//
// 参数
const login_user_name = document.getElementById('username');
const login_password = document.getElementById('password');

const login_message_element = document.createElement('p');
login_message_element.id = 'login-message';
login_message_element.style.textAlign = 'center';
login_message_element.style.marginTop = '10px';

const login_form_container = document.getElementById('login-form-container');
const login_form = document.getElementById('login-form');

if (login_form_container) {
    login_form_container.appendChild(login_message_element);
} else {
    console.error('找不到登录表单容器元素，无法显示消息。');
}

//——————————————————————————————————————————————————————————————————//
//组件函数
const ClearMessages = () => {
    // 清空 //
    login_user_name.value = '';
    login_password.value = '';
};

const PostData = async (url = '', data = {}) => {
    const response_ = await fetch(url, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',

        body: JSON.stringify(data),
    });

    // 检测状态码
    if (!response_.ok) {
        throw new Error(`HTTP ${response_.status} 错误!`);
    }

    return response_.json();
};

//——————————————————————————————————————————————————————————————————//
//函数
/**
 *
 * @param {点击的元素单元} event_
 */
const Summit = (event_) => {
    event_.preventDefault(); // Prevent the default form submission (page reload)

    // 清理信息
    // ClearMessages();
    // 获取注册和登录信息
    const user_name = login_user_name.value;
    const password = login_password.value;

    // 发送信息
    // 编辑信息的账密
    const message_ = {
        user_name: user_name,
        password: password,
    };

    PostData('/login/', message_)
        .then((data) => {
            // 根据后端返回的数据显示不同的消息
            // 后端返回 success:true
            if (data.success) {
                localStorage.setItem('AuthToken', data.token);
                console.log('登录成功!');

                window.location.href = 'Nex/';
            } else {
                console.log('登录失败!');
            }
        })
        .catch((error) => {
            console.error('登录请求失败:', error);
        });
};

//——————————————————————————————————————————————————————————————————//
// 如果存在 DOMContentLoaded 页面加载结束
document.addEventListener('DOMContentLoaded', () => {
    // 假设你的登录按钮有一个 id="login-button"
    if (login_form) {
        login_form.addEventListener('submit', Summit);
    } else {
        console.error('[debug] 找不到登录按钮元素');
    }
});
