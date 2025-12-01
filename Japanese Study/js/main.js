// 移动端菜单交互
const menuToggle = document.getElementById('menuToggle');
const mobileMenu = document.getElementById('mobileMenu');
const closeMenu = document.getElementById('closeMenu');

if (menuToggle && mobileMenu) {
    menuToggle.addEventListener('click', () => {
        mobileMenu.classList.add('open');
        document.body.style.overflow = 'hidden'; // 防止背景滚动
    });
}

if (closeMenu && mobileMenu) {
    closeMenu.addEventListener('click', () => {
        mobileMenu.classList.remove('open');
        document.body.style.overflow = '';
    });
}

// 点击菜单项后关闭菜单
const mobileMenuLinks = document.querySelectorAll('.mobile-menu nav a');
mobileMenuLinks.forEach(link => {
    link.addEventListener('click', () => {
        if (mobileMenu) {
            mobileMenu.classList.remove('open');
            document.body.style.overflow = '';
        }
    });
});

// 高亮当前页面的导航链接
const currentPath = window.location.pathname;
const navLinks = document.querySelectorAll('.nav-links a, .mobile-menu nav a');

navLinks.forEach(link => {
    // 获取链接的路径部分
    const linkPath = new URL(link.href).pathname;
    
    // 比较路径，高亮当前页面
    if (currentPath.endsWith(linkPath) || (currentPath === '/' && linkPath === '/index.html')) {
        link.classList.add('active');
    }
});

// 平滑滚动
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80, // 考虑导航栏高度
                behavior: 'smooth'
            });
        }
    });
});

// 页面加载动画
window.addEventListener('load', () => {
    // 添加一个淡入效果
    document.body.classList.add('loaded');
});

// 本地存储学习进度
function saveProgress(dayNumber) {
    const completedDays = JSON.parse(localStorage.getItem('completedDays') || '[]');
    
    if (!completedDays.includes(dayNumber)) {
        completedDays.push(dayNumber);
        localStorage.setItem('completedDays', JSON.stringify(completedDays));
        
        // 更新进度条
        updateProgressBar(completedDays.length);
        
        // 显示完成消息
        showCompletionMessage();
    }
}

// 更新进度条
function updateProgressBar(completedDays) {
    const progressBar = document.querySelector('.progress-fill');
    const progressStats = document.querySelectorAll('.progress-stats span');
    
    if (progressBar) {
        const percentage = (completedDays / 300) * 100;
        progressBar.style.width = `${percentage}%`;
    }
    
    if (progressStats.length >= 2) {
        progressStats[0].textContent = `已完成：${completedDays}/300 天`;
        progressStats[1].textContent = `完成率：${((completedDays / 300) * 100).toFixed(2)}%`;
    }
}

// 显示完成消息
function showCompletionMessage() {
    // 创建一个消息元素
    const message = document.createElement('div');
    message.className = 'completion-message';
    message.textContent = '恭喜你完成了今天的学习！继续保持！';
    message.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #4CAF50;
        color: white;
        padding: 15px 25px;
        border-radius: 25px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        z-index: 2000;
        animation: slideIn 0.3s ease;
        font-weight: bold;
    `;
    
    // 添加动画样式
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateY(100px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(message);
    
    // 3秒后移除消息
    setTimeout(() => {
        message.style.opacity = '0';
        message.style.transition = 'opacity 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(message);
        }, 300);
    }, 3000);
}

// 完成课程
function completeLesson(dayNumber) {
    saveProgress(dayNumber);
}

// 页面加载时恢复进度
window.addEventListener('DOMContentLoaded', () => {
    const completedDays = JSON.parse(localStorage.getItem('completedDays') || '[]');
    updateProgressBar(completedDays.length);
});

// 回到顶部按钮
const backToTop = document.createElement('button');
backToTop.className = 'back-to-top';
backToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
backToTop.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #e63946;
    color: white;
    border: none;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    font-size: 1.2rem;
    opacity: 0;
    transition: opacity 0.3s ease, transform 0.3s ease;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
`;

document.body.appendChild(backToTop);

window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        backToTop.style.opacity = '1';
        backToTop.style.transform = 'translateY(0)';
    } else {
        backToTop.style.opacity = '0';
        backToTop.style.transform = 'translateY(20px)';
    }
});

backToTop.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});