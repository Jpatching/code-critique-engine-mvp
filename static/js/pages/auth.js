/**
 * Authentication Page
 * Handles login and signup forms
 */

export async function renderAuthPage() {
    const app = document.getElementById('app');
    
    app.innerHTML = `
        <div class="auth-container">
            <div class="auth-card">
                <h2>Code Critique Engine</h2>
                <p class="auth-subtitle">Stop producing AI slop. Build production-ready code.</p>
                
                <div class="auth-tabs">
                    <button class="auth-tab active" data-tab="login">Login</button>
                    <button class="auth-tab" data-tab="signup">Sign Up</button>
                </div>

                <!-- Login Form -->
                <form id="loginForm" class="auth-form">
                    <div class="form-group">
                        <label for="loginEmail">Email</label>
                        <input type="email" id="loginEmail" required>
                    </div>
                    <div class="form-group">
                        <label for="loginPassword">Password</label>
                        <input type="password" id="loginPassword" required>
                    </div>
                    <div class="form-error" id="loginError"></div>
                    <button type="submit" class="btn-primary">Login</button>
                </form>

                <!-- Signup Form -->
                <form id="signupForm" class="auth-form" style="display: none;">
                    <div class="form-group">
                        <label for="signupName">Name</label>
                        <input type="text" id="signupName" required>
                    </div>
                    <div class="form-group">
                        <label for="signupEmail">Email</label>
                        <input type="email" id="signupEmail" required>
                    </div>
                    <div class="form-group">
                        <label for="signupPassword">Password</label>
                        <input type="password" id="signupPassword" required minlength="8">
                        <small>At least 8 characters</small>
                    </div>
                    <div class="form-group">
                        <label for="signupPasswordConfirm">Confirm Password</label>
                        <input type="password" id="signupPasswordConfirm" required minlength="8">
                        <small id="passwordMatchHint" class="password-hint"></small>
                    </div>
                    <div class="form-error" id="signupError"></div>
                    <button type="submit" class="btn-primary">Sign Up</button>
                </form>
            </div>
        </div>
    `;

    // Setup tab switching
    const tabs = document.querySelectorAll('.auth-tab');
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            const tabName = tab.getAttribute('data-tab');
            if (tabName === 'login') {
                loginForm.style.display = 'block';
                signupForm.style.display = 'none';
            } else {
                loginForm.style.display = 'none';
                signupForm.style.display = 'block';
            }
        });
    });

    // Handle login
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        const errorDiv = document.getElementById('loginError');

        errorDiv.textContent = '';
        const btn = loginForm.querySelector('button');
        btn.textContent = 'Logging in...';
        btn.disabled = true;

        const result = await authService.login(email, password);
        
        if (result.success) {
            router.navigate('/dashboard');
        } else {
            errorDiv.textContent = result.error;
            btn.textContent = 'Login';
            btn.disabled = false;
        }
    });

    // Handle signup
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('signupName').value;
        const email = document.getElementById('signupEmail').value;
        const password = document.getElementById('signupPassword').value;
        const passwordConfirm = document.getElementById('signupPasswordConfirm').value;
        const errorDiv = document.getElementById('signupError');

        errorDiv.textContent = '';
        
        // Client-side validation
        if (password !== passwordConfirm) {
            errorDiv.textContent = 'Passwords do not match';
            return;
        }
        
        const btn = signupForm.querySelector('button');
        btn.textContent = 'Creating account...';
        btn.disabled = true;

        const result = await authService.signup(name, email, password, passwordConfirm);
        
        if (result.success) {
            router.navigate('/dashboard');
        } else {
            errorDiv.textContent = result.error;
            btn.textContent = 'Sign Up';
            btn.disabled = false;
        }
    });
    
    // Add real-time password matching feedback
    const passwordInput = document.getElementById('signupPassword');
    const passwordConfirmInput = document.getElementById('signupPasswordConfirm');
    const passwordMatchHint = document.getElementById('passwordMatchHint');
    
    const checkPasswordMatch = () => {
        const password = passwordInput.value;
        const passwordConfirm = passwordConfirmInput.value;
        
        if (!passwordConfirm) {
            passwordMatchHint.textContent = '';
            passwordMatchHint.className = 'password-hint';
            return;
        }
        
        if (password === passwordConfirm) {
            passwordMatchHint.textContent = '✓ Passwords match';
            passwordMatchHint.className = 'password-hint match';
        } else {
            passwordMatchHint.textContent = '✗ Passwords do not match';
            passwordMatchHint.className = 'password-hint no-match';
        }
    };
    
    passwordInput.addEventListener('input', checkPasswordMatch);
    passwordConfirmInput.addEventListener('input', checkPasswordMatch);
}
