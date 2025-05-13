// 获取注册表的id
const login_container_id = document.getElementById('login-form-container')
const register_container_id = document.getElementById('register-form-container')

// 获取按钮id
const register_new_link = document.getElementById('register-new-link')
const return_login_link = document.getElementById('return-login-link')

/**
 * 点击显示注册表 隐层
 */
register_new_link.addEventListener('click',(event_)=>
{
    // 防止默认跳转
    event_.preventDefault();

    // 隐藏
    login_container_id.classList.add('hidden');

    // 显示
    register_container_id.classList.remove('hidden');
})

return_login_link.addEventListener('click',(event_)=>
{
    // 防止默认跳转
    event_.preventDefault();

    // 隐藏
    register_container_id.classList.add('hidden');

    // 显示
    login_container_id.classList.remove('hidden');
})

