<template>
  <div class="auth-wrapper">
    <div class="container" :class="{ 'right-panel-active': isPanelActive }">
      <div class="form-container sign-up-container">
        <form @submit.prevent="handleRegister">
          <h1>Create Account</h1>
          <div class="social-container">
            <a href="#" class="social"><i class="fab fa-facebook-f"></i></a>
            <a href="#" class="social"><i class="fab fa-google-plus-g"></i></a>
            <a href="#" class="social"><i class="fab fa-linkedin-in"></i></a>
          </div>
          <span>or use your email for registration</span>

          <!-- Error/Success Messages -->
          <div v-if="errorMessage" class="message error-message">
            {{ errorMessage }}
          </div>
          <div v-if="successMessage" class="message success-message">
            {{ successMessage }}
          </div>

          <input
            type="text"
            v-model="registerForm.name"
            placeholder="Name"
            required
          />
          <input
            type="email"
            v-model="registerForm.email"
            placeholder="Email"
            required
          />
          <input
            type="password"
            v-model="registerForm.password"
            placeholder="Password"
            required
          />
          <button type="submit" :disabled="isLoading">
            {{ isLoading ? "Signing Up..." : "Sign Up" }}
          </button>
        </form>
      </div>

      <div class="form-container sign-in-container">
        <form @submit.prevent="handleLogin">
          <h1>Sign in</h1>
          <div class="social-container">
            <a href="#" class="social"><i class="fab fa-facebook-f"></i></a>
            <a href="#" class="social"><i class="fab fa-google-plus-g"></i></a>
            <a href="#" class="social"><i class="fab fa-linkedin-in"></i></a>
          </div>
          <span>or use your account</span>

          <!-- Error/Success Messages -->
          <div v-if="errorMessage" class="message error-message">
            {{ errorMessage }}
          </div>
          <div v-if="successMessage" class="message success-message">
            {{ successMessage }}
          </div>

          <input
            type="email"
            v-model="loginForm.email"
            placeholder="Email"
            required
          />
          <input
            type="password"
            v-model="loginForm.password"
            placeholder="Password"
            required
          />
          <a href="#" class="forgot-link">Forgot your password?</a>
          <button type="submit" :disabled="isLoading">
            {{ isLoading ? "Signing In..." : "Sign In" }}
          </button>
        </form>
      </div>

      <div class="overlay-container">
        <div class="overlay">
          <div class="overlay-panel overlay-left">
            <h1>Welcome Back!</h1>
            <p>
              To keep connected with us please login with your personal info
            </p>
            <button class="ghost" @click="deactivatePanel">Sign In</button>
          </div>
          <div class="overlay-panel overlay-right">
            <h1>Hello, Friend!</h1>
            <p>Enter your personal details and start your journey with us</p>
            <button class="ghost" @click="activatePanel">Sign Up</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AuthFormComponent",
  data() {
    return {
      isPanelActive: false,
      loginForm: { email: "", password: "" },
      registerForm: { name: "", email: "", password: "" },
      isLoading: false,
      errorMessage: "",
      successMessage: "",
    };
  },
  methods: {
    activatePanel() {
      this.isPanelActive = true;
      this.clearMessages();
    },
    deactivatePanel() {
      this.isPanelActive = false;
      this.clearMessages();
    },
    clearMessages() {
      this.errorMessage = "";
      this.successMessage = "";
    },

    // Cookie utility methods
    setCookie(name, value, days = 7) {
      const expires = new Date();
      expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
      const cookieString = `${name}=${value}; expires=${expires.toUTCString()}; path=/; SameSite=Lax`;
      document.cookie = cookieString;
    },

    getCookie(name) {
      const nameEQ = name + "=";
      const ca = document.cookie.split(";");
      for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === " ") c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) {
          return c.substring(nameEQ.length, c.length);
        }
      }
      return null;
    },

    deleteCookie(name) {
      document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; SameSite=Lax`;
    },

    // JWT utility methods
    setAuthToken(token) {
      // Store in cookie
      this.setCookie("auth_token", token, 7);

      // Also store in localStorage
      try {
        localStorage.setItem("auth_token", token);
      } catch (error) {
        console.error("Error storing in localStorage:", error);
      }

      // Set default axios header for future requests
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    },

    getAuthToken() {
      // Try to get from cookie first, then localStorage
      const cookieToken = this.getCookie("auth_token");
      const localStorageToken = localStorage.getItem("auth_token");
      return cookieToken || localStorageToken;
    },

    removeAuthToken() {
      // Remove from cookie
      this.deleteCookie("auth_token");

      // Remove from localStorage
      try {
        localStorage.removeItem("auth_token");
      } catch (error) {
        console.error("Error removing from localStorage:", error);
      }

      // Remove from axios default headers
      delete axios.defaults.headers.common["Authorization"];
    },

    // Check if user is authenticated
    isAuthenticated() {
      const token = this.getAuthToken();
      if (!token) return false;

      try {
        // Simple JWT expiry check
        const payload = JSON.parse(atob(token.split(".")[1]));
        const currentTime = Math.floor(Date.now() / 1000);
        return payload.exp > currentTime;
      } catch (error) {
        console.error("Invalid token format:", error);
        this.removeAuthToken();
        return false;
      }
    },

    // Get user info from JWT
    getUserInfo() {
      const token = this.getAuthToken();
      if (!token) return null;

      try {
        const payload = JSON.parse(atob(token.split(".")[1]));
        return {
          id: payload.id || payload.userId,
          email: payload.email,
          name: payload.name || payload.username,
          exp: payload.exp,
        };
      } catch (error) {
        console.error("Error parsing token:", error);
        return null;
      }
    },

    // Ganti method handleLogin Anda dengan ini:
    async handleLogin() {
      this.clearMessages();

      if (!this.loginForm.email || !this.loginForm.password) {
        this.errorMessage = "Please fill in all fields";
        return;
      }

      this.isLoading = true;

      try {
        // Anda bisa tetap menggunakan simulasi atau API call yang sebenarnya
        // Uncomment baris di bawah untuk menggunakan API call Anda
        const response = await axios.post(
          "http://localhost:3000/api/users/login",
          this.loginForm
        );

        // const response = await this.simulateLoginResponse(); // Gunakan ini untuk testing

        this.successMessage = "Login successful! Redirecting...";

        // Cek dan simpan JWT token
        if (response.data.token) {
          this.setAuthToken(response.data.token);
        } else {
          // Jika tidak ada token, lempar error agar ditangkap oleh blok catch
          throw new Error("Token not found in login response");
        }

        // Reset form login
        this.loginForm = { email: "", password: "" };

        // --- INI PERBAIKANNYA ---
        // Tunggu 1 detik untuk user bisa melihat pesan sukses,
        // lalu alihkan ke halaman dashboard.
        setTimeout(() => {
          // Gunakan $router.push untuk mengalihkan ke rute bernama 'Dashboard'.
          // Pastikan nama rute ini sesuai dengan yang ada di router/index.js Anda.
          this.$router.push({ name: "dashboard" });
        }, 1000);
      } catch (error) {
        console.error("Login error:", error);
        // Hapus token yang mungkin salah/kadaluwarsa jika login gagal
        this.removeAuthToken();

        if (error.response?.data?.message) {
          this.errorMessage = error.response.data.message;
        } else {
          this.errorMessage =
            error.message || "Login failed. Please try again.";
        }
      } finally {
        this.isLoading = false;
      }
    },

    async handleRegister() {
      this.clearMessages();

      if (
        !this.registerForm.name ||
        !this.registerForm.email ||
        !this.registerForm.password
      ) {
        this.errorMessage = "Please fill in all fields";
        return;
      }

      this.isLoading = true;

      try {
        // Simulasi response untuk testing (ganti dengan API call yang sebenarnya)
        const response = await this.simulateRegisterResponse();

        /* Uncomment untuk API call yang sebenarnya:
        const response = await axios.post(
          "http://localhost:3000/api/users/register",
          {
            username: this.registerForm.name,
            email: this.registerForm.email,
            password: this.registerForm.password,
          }
        );
        */

        this.successMessage = "Registration successful! Please sign in.";

        // Reset form
        this.registerForm = { name: "", email: "", password: "" };

        // Switch to login panel
        setTimeout(() => {
          this.deactivatePanel();
        }, 2000);
      } catch (error) {
        console.error("Register error:", error);
        if (error.response?.data?.message) {
          this.errorMessage = error.response.data.message;
        } else {
          this.errorMessage = "Registration failed. Please try again.";
        }
      } finally {
        this.isLoading = false;
      }
    },

    // Simulasi responses untuk testing
    async simulateLoginResponse() {
      return new Promise((resolve) => {
        setTimeout(() => {
          // Simulasi JWT token (dalam praktik nyata, ini akan datang dari server)
          const mockToken = this.generateMockJWT();
          resolve({
            data: {
              token: mockToken,
              user: {
                id: 1,
                email: this.loginForm.email,
                name: "Test User",
              },
            },
          });
        }, 1000);
      });
    },

    async simulateRegisterResponse() {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            data: {
              message: "User registered successfully",
              user: {
                id: 1,
                email: this.registerForm.email,
                name: this.registerForm.name,
              },
            },
          });
        }, 1000);
      });
    },

    // Generate mock JWT untuk testing
    generateMockJWT() {
      const header = { alg: "HS256", typ: "JWT" };
      const payload = {
        id: 1,
        email: this.loginForm.email,
        name: "Test User",
        iat: Math.floor(Date.now() / 1000),
        exp: Math.floor(Date.now() / 1000) + 60 * 60 * 24 * 7, // 7 days
      };

      const encodedHeader = btoa(JSON.stringify(header));
      const encodedPayload = btoa(JSON.stringify(payload));
      const signature = "mock_signature";

      return `${encodedHeader}.${encodedPayload}.${signature}`;
    },

    // Logout method
    logout() {
      this.removeAuthToken();
      this.$emit("logout");
    },
  },

  // Set up axios interceptor when component mounts
  mounted() {
    // Set token in axios header if it exists
    const token = this.getAuthToken();
    if (token && this.isAuthenticated()) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    }

    // Add response interceptor to handle token expiry
    axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          this.removeAuthToken();
          this.$emit("token-expired");
        }
        return Promise.reject(error);
      }
    );
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap");

/* Reset default margins and paddings */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body,
html {
  height: 100%;
  margin: 0;
  padding: 0;
}

.auth-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: "Poppins", sans-serif;
  min-height: 100vh;
  height: 100vh;
  width: 100vw;
  padding: 0;
  margin: 0;
  position: fixed;
  top: 0;
  left: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

h1 {
  font-weight: 700;
  margin: 0 0 20px;
  color: #333;
  font-size: 28px;
}

p {
  font-size: 14px;
  font-weight: 300;
  line-height: 22px;
  letter-spacing: 0.3px;
  margin: 20px 0 25px;
}

span {
  font-size: 12px;
  color: #666;
  margin: 15px 0;
}

a {
  color: #4fc3f7;
  font-size: 13px;
  text-decoration: none;
  transition: color 0.3s ease;
}

a:hover {
  color: #29b6f6;
}

.forgot-link {
  margin: 15px 0;
}

button {
  border-radius: 25px;
  border: 1px solid #4fc3f7;
  background: linear-gradient(45deg, #4fc3f7, #29b6f6);
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  padding: 14px 45px;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: all 0.3s ease;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(79, 195, 247, 0.3);
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(79, 195, 247, 0.4);
}

button:active {
  transform: translateY(0);
}

button.ghost {
  background: transparent;
  border: 2px solid #fff;
  box-shadow: none;
}

button.ghost:hover {
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2);
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

button:disabled:hover {
  transform: none;
  box-shadow: 0 4px 15px rgba(79, 195, 247, 0.3);
}

/* Message Styles */
.message {
  width: 100%;
  padding: 10px 15px;
  border-radius: 8px;
  margin: 10px 0;
  font-size: 13px;
  font-weight: 500;
  text-align: center;
}

.error-message {
  background-color: #fee;
  color: #dc3545;
  border: 1px solid #f5c6cb;
}

.success-message {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

form {
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 0 40px;
  height: 100%;
  text-align: center;
  border-radius: 10px 0 0 10px;
}

input {
  background: #f8f9fa;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 14px 18px;
  margin: 6px 0;
  width: 100%;
  font-size: 14px;
  transition: all 0.3s ease;
  outline: none;
}

input:focus {
  border-color: #4fc3f7;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(79, 195, 247, 0.1);
}

.container {
  background: #fff;
  border-radius: 15px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  position: relative;
  overflow: hidden;
  width: 768px;
  max-width: 90vw;
  min-height: 480px;
  transform: translate(0, 0);
}

.form-container {
  position: absolute;
  top: 0;
  height: 100%;
  transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.sign-in-container {
  left: 0;
  width: 50%;
  z-index: 2;
}

.sign-up-container {
  left: 0;
  width: 50%;
  opacity: 0;
  z-index: 1;
}

.overlay-container {
  position: absolute;
  top: 0;
  left: 50%;
  width: 50%;
  height: 100%;
  overflow: hidden;
  transition: transform 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  z-index: 100;
}

.overlay {
  background: linear-gradient(135deg, #4fc3f7 0%, #29b6f6 50%, #03a9f4 100%);
  color: #fff;
  position: relative;
  left: -100%;
  height: 100%;
  width: 200%;
  transform: translateX(0);
  transition: transform 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  border-radius: 0 15px 15px 0;
}

.overlay-panel {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 0 35px;
  text-align: center;
  top: 0;
  height: 100%;
  width: 50%;
  transform: translateX(0);
  transition: transform 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.overlay-left {
  transform: translateX(-20%);
}
.overlay-right {
  right: 0;
  transform: translateX(0);
}

.social-container {
  margin: 20px 0;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.social {
  border: 1px solid #e0e0e0;
  border-radius: 50%;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  height: 40px;
  width: 40px;
  background: #fff;
  transition: all 0.3s ease;
  color: #666;
}

.social:hover {
  background: #4fc3f7;
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 195, 247, 0.3);
}

/* Animations */
.container.right-panel-active .sign-in-container {
  transform: translateX(100%);
}
.container.right-panel-active .overlay-container {
  transform: translateX(-100%);
}
.container.right-panel-active .sign-up-container {
  transform: translateX(100%);
  opacity: 1;
  z-index: 5;
  animation: fadeIn 0.6s;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
    z-index: 1;
  }
  50% {
    opacity: 0;
    z-index: 1;
  }
  100% {
    opacity: 1;
    z-index: 5;
  }
}

.container.right-panel-active .overlay {
  transform: translateX(50%);
}
.container.right-panel-active .overlay-left {
  transform: translateX(0);
}
.container.right-panel-active .overlay-right {
  transform: translateX(20%);
}

/* Responsive */
@media (max-width: 768px) {
  .container {
    min-height: 600px;
    max-width: 95vw;
  }
  form {
    padding: 0 25px;
  }
  .overlay-panel {
    padding: 0 25px;
  }
}

@media (max-width: 480px) {
  .container {
    width: 100vw;
    max-width: 100vw;
    border-radius: 0;
    min-height: 100vh;
  }

  .auth-wrapper {
    padding: 0;
  }
}
</style>
