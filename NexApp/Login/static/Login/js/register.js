// ——————————————————————————————————————————————————————————————————————————————————
// 参数
const register_form = document.getElementById('register-form');
const message_el = document.getElementById('register-message');
const submit_btn = document.getElementById('register-button');
const loading_spinner = submit_btn.querySelector('.loading-spinner');

// ——————————————————————————————————————————————————————————————————————————————————
// 组件函数
/**
 *
 * @param {boolean} is_loading
 */
const set_loading = (is_loading) => {
    submit_btn.disabled = is_loading;
    loading_spinner.classList.toggle('hidden', !is_loading);
    submit_btn.querySelector('.button-text').textContent = is_loading
        ? '提交中...'
        : '立即注册';
};

/**
 *
 * @param {string} text
 * @param {boolean} is_error
 */
const show_message = (text, is_error = true) => {
    message_el.textContent = text;
    message_el.className = `message-box ${is_error ? 'error' : 'success'}`;
    message_el.style.display = 'block';
};

// 密码强度校验
const validate_password = (password) => {
    const strongRegex =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return strongRegex.test(password);
};

// ——————————————————————————————————————————————————————————————————————————————————
// 主要业务函数
// 上交函数

/**
 *  Object.values(): 这是 JavaScript 的一个内置方法。
 *  它接收一个对象作为参数，然后返回一个包含该对象 自身 可枚举属性 值 的 数组。它会忽略对象的键（keys）。
 *  对于上面的例子 data.errors = { "user_name": "用户名已存在", "email": "邮箱已被注册" }，
 *  Object.values(data.errors) 的结果将是一个数组：
 *  ["用户名已存在", "邮箱已被注册"]
 *
 *
 * @param {Event} e
 * @returns
 */
const Submit = async (e) => {
    e.preventDefault();

    // 获取表单数据
    const form_data = {
        user_name: document.getElementById('register-username').value.trim(),
        email: document.getElementById('register-email').value.trim(),
        password: document.getElementById('register-password').value,
        password_confirm: document.getElementById('register-password-confirm')
            .value,
    };

    // 客户端验证
    if (!form_data.user_name || !form_data.email || !form_data.password) {
        show_message('所有字段均为必填项');
        return;
    }

    if (form_data.password !== form_data.password_confirm) {
        show_message('两次密码输入不一致');
        return;
    }

    if (!validate_password(form_data.password)) {
        show_message('密码需至少8位,包含大小写字母、数字和特殊符号');
        return;
    }

    try {
        set_loading(true);

        const response = await fetch('/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(form_data),
        });

        const data = await response.json();
        if (response.ok) {
            // Status 200-299
            if (data.success) {
                show_message('注册成功！3秒后跳转至登录页', false);
            } else {
                if (data.errors) {
                    const error_messages = Object.values(data.errors).join(
                        '\n'
                    );
                    show_message(error_messages || '注册失败，请检查输入');
                } else {
                    show_message(data.message || '注册失败，请检查输入');
                }
            }
        } else {
            let error_text = `服务器错误 (${response.status})`;
            if (data && data.errors) {
                const error_messages = Object.values(data.errors).join('\n');
                error_text = error_messages || `注册失败 (${response.status})`;
            } else if (data && data.message) {
                error_text = data.message;
            } else {
                error_text = `请求失败: ${
                    response.statusText || response.status
                }`;
            }
            show_message(error_text);
        }
    } catch (error) {
        show_message('网络连接异常，请稍后重试');
    } finally {
        set_loading(false);
    }
};

// ——————————————————————————————————————————————————————————————————————————————————
// 初始化
document.addEventListener('DOMContentLoaded', () => {
    if (register_form) {
        register_form.addEventListener('submit', Submit);
    }
});
