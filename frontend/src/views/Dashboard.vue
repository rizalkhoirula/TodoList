<template>
  <div class="dashboard-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo-container">
          <i class="bi bi-grid-3x3-gap-fill logo-icon"></i>
          <span class="logo-text">Dashboard</span>
        </div>
      </div>
      <nav class="nav-section">
        <ul class="nav-links">
          <li
            :class="{ active: activeView === 'home' }"
            @click="changeView('home')"
          >
            <a href="#" @click.prevent>
              <i class="bi bi-house-door-fill"></i>
              <span class="nav-text">Home</span>
            </a>
          </li>
          <li
            :class="{ active: activeView === 'tasks' }"
            @click="changeView('tasks')"
          >
            <a href="#" @click.prevent>
              <i class="bi bi-list-task"></i>
              <span class="nav-text">Tasks</span>
            </a>
          </li>
          <li
            :class="{ active: activeView === 'categories' }"
            @click="changeView('categories')"
          >
            <a href="#" @click.prevent>
              <i class="bi bi-tags-fill"></i>
              <span class="nav-text">Categories</span>
            </a>
          </li>
        </ul>
      </nav>
    </aside>

    <main class="main-content">
      <header class="main-header">
        <div class="header-title">
          <h2>{{ headerTitle }}</h2>
          <p class="header-subtitle">
            Welcome back, manage your tasks efficiently
          </p>
        </div>
        <div class="user-menu" :class="{ 'dropdown-open': dropdownOpen }">
          <button class="user-menu-btn" type="button" @click="toggleDropdown">
            <img
              src="https://i.pravatar.cc/40?img=3"
              alt="User"
              class="user-avatar"
            />
            <div class="user-info">
              <span class="user-name">Alex Yara</span>
              <span class="user-role">Admin</span>
            </div>
            <i
              class="bi bi-chevron-down dropdown-icon"
              :class="{ rotated: dropdownOpen }"
            ></i>
          </button>
          <div class="dropdown-menu" v-show="dropdownOpen">
            <a class="dropdown-item" href="#" @click.prevent="editUser">
              <i class="bi bi-person-gear"></i>
              <span>Edit Profile</span>
            </a>
            <a class="dropdown-item" href="#" @click.prevent="showSettings">
              <i class="bi bi-gear-fill"></i>
              <span>Settings</span>
            </a>
            <div class="dropdown-divider"></div>
            <a
              class="dropdown-item logout-item"
              href="#"
              @click.prevent="logout"
            >
              <i class="bi bi-box-arrow-right"></i>
              <span>Logout</span>
            </a>
          </div>
        </div>
      </header>

      <div class="content-body">
        <div v-if="activeView === 'home'" class="view-home">
          <!-- Loading state -->
          <div v-if="loading" class="loading-state">
            <div class="spinner"></div>
            <p>Loading dashboard data...</p>
          </div>

          <div v-else class="stats-grid">
            <div class="stat-card">
              <div class="stat-content">
                <div class="stat-icon bg-gradient-primary">
                  <i class="bi bi-check2-circle"></i>
                </div>
                <div class="stat-info">
                  <p class="stat-label">Total Tasks</p>
                  <h3 class="stat-number">{{ apiData.totalTasks || 0 }}</h3>
                </div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-content">
                <div class="stat-icon bg-gradient-success">
                  <i class="bi bi-trophy-fill"></i>
                </div>
                <div class="stat-info">
                  <p class="stat-label">Completed</p>
                  <h3 class="stat-number">{{ apiData.completedTasks || 0 }}</h3>
                </div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-content">
                <div class="stat-icon bg-gradient-warning">
                  <i class="bi bi-clock-fill"></i>
                </div>
                <div class="stat-info">
                  <p class="stat-label">Upcoming</p>
                  <h3 class="stat-number">{{ apiData.upcomingTasks || 0 }}</h3>
                </div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-content">
                <div class="stat-icon bg-gradient-danger">
                  <i class="bi bi-exclamation-octagon-fill"></i>
                </div>
                <div class="stat-info">
                  <p class="stat-label">Overdue</p>
                  <h3 class="stat-number">{{ apiData.overdueTasks || 0 }}</h3>
                </div>
              </div>
            </div>
          </div>

          <div class="content-grid">
            <div class="deadlines-card">
              <div class="card-header">
                <div class="card-title">
                  <i class="bi bi-exclamation-triangle-fill"></i>
                  <h3>Upcoming Deadlines</h3>
                </div>
              </div>
              <div class="card-body">
                <div class="deadline-list">
                  <div
                    v-for="task in upcomingTasks"
                    :key="task.id"
                    class="deadline-item"
                  >
                    <div class="deadline-info">
                      <h4 class="task-name">{{ task.name }}</h4>
                      <p class="task-category">{{ task.category }}</p>
                    </div>
                    <div class="deadline-date">
                      <span class="date-badge">{{
                        formatDate(task.dueDate)
                      }}</span>
                    </div>
                  </div>
                  <div v-if="upcomingTasks.length === 0" class="empty-state">
                    <i class="bi bi-check-circle-fill"></i>
                    <p>No upcoming deadlines. Great job!</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="activity-card">
              <div class="card-header">
                <div class="card-title">
                  <i class="bi bi-activity"></i>
                  <h3>Recent Activity</h3>
                </div>
              </div>
              <div class="card-body">
                <!-- Loading state untuk recent activity -->
                <div v-if="loading" class="loading-state">
                  <div class="spinner-sm"></div>
                  <p>Loading activities...</p>
                </div>

                <div v-else class="activity-list">
                  <div
                    v-for="activity in recentActivities"
                    :key="activity.id"
                    class="activity-item"
                  >
                    <div class="activity-icon" :class="activity.iconBgClass">
                      <i :class="'bi ' + activity.icon"></i>
                    </div>
                    <div class="activity-content">
                      <p class="activity-text">{{ activity.text }}</p>
                      <span class="activity-time">{{ activity.time }}</span>
                    </div>
                  </div>

                  <!-- Empty state -->
                  <div v-if="recentActivities.length === 0" class="empty-state">
                    <i class="bi bi-clock-history"></i>
                    <p>No recent activity to show.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activeView === 'tasks'" class="view-table">
          <div class="table-card">
            <div class="card-header">
              <div class="card-title">
                <h3>Task Management</h3>
                <p>Manage and track all your tasks</p>
              </div>
              <div class="header-actions">
                <div
                  class="task-filter-dropdown"
                  :class="{ 'dropdown-open': showTaskDropdown }"
                >
                  <button class="filter-btn" @click="toggleTaskDropdown">
                    <span>{{ selectedTaskView }}</span>
                    <i
                      class="bi bi-chevron-down dropdown-icon"
                      :class="{ rotated: showTaskDropdown }"
                    ></i>
                  </button>
                  <div class="filter-dropdown-menu" v-show="showTaskDropdown">
                    <a
                      v-for="option in taskDropdownOptions"
                      :key="option"
                      class="filter-dropdown-item"
                      :class="{ active: selectedTaskView === option }"
                      href="#"
                      @click.prevent="selectTaskView(option)"
                    >
                      {{ option }}
                    </a>
                  </div>
                </div>
                <button class="add-task-btn" @click="openAddTaskForm">
                  <i class="bi bi-plus-circle"></i>
                  <span>Add Task</span>
                </button>
                <div class="search-container">
                  <div class="search-box">
                    <i class="bi bi-search"></i>
                    <input
                      type="text"
                      placeholder="Search tasks..."
                      v-model="searchTaskQuery"
                    />
                  </div>
                </div>
              </div>
            </div>
            <div class="card-body">
              <div class="table-container">
                <table class="modern-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Task Name</th>
                      <th>Category</th>
                      <th>Due Date</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="task in displayedTasks" :key="task.id">
                      <td>
                        <span class="id-badge">#{{ task.id }}</span>
                      </td>
                      <td>
                        <div class="task-cell">
                          <strong>{{ task.name }}</strong>
                        </div>
                      </td>
                      <td>
                        <div
                          class="dropdown-cell"
                          :class="{
                            'dropdown-open': taskCategoryDropdowns[task.id],
                          }"
                        >
                          <button
                            class="cell-dropdown-btn category-badge"
                            :class="getCategoryClass(task.category)"
                            @click="toggleCategoryDropdown(task.id)"
                          >
                            {{ task.category }}
                            <i class="bi bi-chevron-down"></i>
                          </button>
                          <div
                            class="cell-dropdown-menu"
                            v-show="taskCategoryDropdowns[task.id]"
                          >
                            <a
                              v-for="category in categories"
                              :key="category.id"
                              class="cell-dropdown-item"
                              href="#"
                              @click.prevent="
                                updateTaskCategory(task.id, category.id)
                              "
                            >
                              <span
                                class="category-badge"
                                :class="getCategoryClass(category.name)"
                                >{{ category.name }}</span
                              >
                            </a>
                          </div>
                        </div>
                      </td>
                      <td>{{ formatDate(task.dueDate) }}</td>
                      <td>
                        <div
                          class="dropdown-cell"
                          :class="{
                            'dropdown-open': taskStatusDropdowns[task.id],
                          }"
                        >
                          <button
                            class="cell-dropdown-btn status-badge"
                            :class="getStatusClass(task.status)"
                            @click="toggleStatusDropdown(task.id)"
                          >
                            {{ task.status }}
                            <i class="bi bi-chevron-down"></i>
                          </button>
                          <div
                            class="cell-dropdown-menu"
                            v-show="taskStatusDropdowns[task.id]"
                          >
                            <a
                              v-for="status in statusOptions"
                              :key="status"
                              class="cell-dropdown-item"
                              href="#"
                              @click.prevent="updateTaskStatus(task.id, status)"
                            >
                              <span
                                class="status-badge"
                                :class="getStatusClass(status)"
                                >{{ status }}</span
                              >
                            </a>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr v-if="displayedTasks.length === 0">
                      <td colspan="5" class="empty-row">
                        <div class="empty-state">
                          <i class="bi bi-search"></i>
                          <p>No tasks found matching your criteria.</p>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activeView === 'categories'" class="view-table">
          <div class="table-card">
            <div class="card-header">
              <div class="card-title">
                <h3>Category Management</h3>
                <p>Organize your tasks with categories</p>
              </div>
              <div class="search-container">
                <div class="search-box">
                  <i class="bi bi-search"></i>
                  <input
                    type="text"
                    placeholder="Search categories..."
                    v-model="searchCategoryQuery"
                  />
                </div>
              </div>
            </div>
            <div class="card-body">
              <div class="table-container">
                <table class="modern-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Category Name</th>
                      <th>Tasks Count</th>
                      <th>Color</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="category in filteredCategories"
                      :key="category.id"
                    >
                      <td>
                        <span class="id-badge">#{{ category.id }}</span>
                      </td>
                      <td>
                        <div class="category-cell">
                          <strong>{{ category.name }}</strong>
                        </div>
                      </td>
                      <td>{{ getTaskCountByCategory(category.name) }}</td>
                      <td>
                        <span
                          class="color-dot"
                          :style="{
                            'background-color': getCategoryClass(
                              category.name,
                              true
                            ),
                          }"
                        ></span>
                      </td>
                    </tr>
                    <tr v-if="filteredCategories.length === 0">
                      <td colspan="4" class="empty-row">
                        <div class="empty-state">
                          <i class="bi bi-search"></i>
                          <p>No categories found matching your search.</p>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <div
      v-if="showAddTaskForm"
      class="modal-overlay"
      @click.self="closeAddTaskForm"
    >
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h3>Add New Task</h3>
          <button class="modal-close-btn" @click="closeAddTaskForm">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="addNewTask">
            <div class="form-group">
              <label for="taskTitle">Task Title *</label>
              <input
                id="taskTitle"
                type="text"
                v-model="newTask.title"
                placeholder="Enter task title"
                required
              />
            </div>
            <div class="form-group">
              <label for="taskDescription">Description</label>
              <textarea
                id="taskDescription"
                v-model="newTask.description"
                placeholder="Enter task description"
                rows="3"
              ></textarea>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="taskCategory">Category *</label>
                <select id="taskCategory" v-model="newTask.categoryId" required>
                  <option disabled value="">Select Category</option>
                  <option
                    v-for="category in categories"
                    :key="category.id"
                    :value="category.id"
                  >
                    {{ category.name }}
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label for="taskStatus">Status</label>
                <select id="taskStatus" v-model="newTask.status">
                  <option value="pending">Pending</option>
                  <option value="in-progress">In Progress</option>
                  <option value="completed">Completed</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label for="taskDeadline">Deadline *</label>
              <input
                id="taskDeadline"
                type="date"
                v-model="newTask.deadline"
                required
              />
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            @click="closeAddTaskForm"
          >
            Cancel
          </button>
          <button type="button" class="btn btn-primary" @click="addNewTask">
            <i class="bi bi-plus-circle"></i>
            Add Task
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ModernDashboard",
  data() {
    return {
      activeView: "home",
      searchTaskQuery: "",
      searchCategoryQuery: "",
      dropdownOpen: false,
      showAddTaskForm: false,
      showTaskDropdown: false,
      taskDropdownOptions: ["All Tasks", "Active Tasks", "History Tasks"],
      selectedTaskView: "All Tasks",
      taskStatusDropdowns: {},
      taskCategoryDropdowns: {},
      loading: false,
      userId: null,
      // API data
      apiData: {
        totalTasks: 0,
        completedTasks: 0,
        upcomingTasks: 0,
        overdueTasks: 0,
      },
      newTask: {
        title: "",
        description: "",
        status: "pending",
        userId: 1,
        categoryId: "",
        deadline: "",
      },
      // Initialize empty arrays - akan diisi dari API
      tasks: [],
      categories: [],
      recentActivities: [],
    };
  },
  computed: {
    headerTitle() {
      const titles = {
        home: "Dashboard Overview",
        tasks: "Task Management",
        categories: "Category Management",
      };
      return titles[this.activeView] || "Dashboard";
    },
    totalTasks() {
      return this.tasks.length;
    },
    completedTasks() {
      return this.tasks.filter((task) => task.completed).length;
    },
    overdueTasks() {
      const now = new Date();
      now.setHours(0, 0, 0, 0);
      return this.tasks.filter((task) => {
        const dueDate = new Date(task.dueDate);
        return dueDate < now && !task.completed;
      });
    },
    upcomingTasks() {
      const now = new Date();
      const sevenDaysFromNow = new Date();
      sevenDaysFromNow.setDate(now.getDate() + 7);
      now.setHours(0, 0, 0, 0);

      return this.tasks
        .filter((task) => {
          const dueDate = new Date(task.dueDate);
          return (
            dueDate >= now && dueDate <= sevenDaysFromNow && !task.completed
          );
        })
        .sort((a, b) => new Date(a.dueDate) - new Date(b.dueDate));
    },
    statusOptions() {
      return ["pending", "in-progress", "completed"];
    },
    activeTasks() {
      return this.tasks.filter((task) => !task.completed);
    },
    historyTasks() {
      return this.tasks.filter((task) => task.completed);
    },
    displayedTasks() {
      let tasksToShow;
      switch (this.selectedTaskView) {
        case "Active Tasks":
          tasksToShow = this.activeTasks;
          break;
        case "History Tasks":
          tasksToShow = this.historyTasks;
          break;
        default:
          tasksToShow = this.tasks;
      }
      if (!this.searchTaskQuery) {
        return tasksToShow;
      }
      const query = this.searchTaskQuery.toLowerCase();
      return tasksToShow.filter(
        (task) =>
          task.name.toLowerCase().includes(query) ||
          task.category.toLowerCase().includes(query)
      );
    },
    filteredCategories() {
      if (!this.searchCategoryQuery) return this.categories;
      const query = this.searchCategoryQuery.toLowerCase();
      return this.categories.filter((category) =>
        category.name.toLowerCase().includes(query)
      );
    },
  },
  methods: {
    async fetchRecentActivity() {
      if (!this.userId) {
        console.error("No userId available for recent activity fetch");
        return;
      }

      try {
        console.log("Fetching recent activity for user:", this.userId);
        const response = await this.makeAuthenticatedRequest(
          `http://localhost:3000/api/tasks/recent-activity?userId=${this.userId}`
        );

        if (response && response.recentActivities) {
          console.log("Recent activity API response:", response);

          // Transform API data to match component structure
          this.recentActivities = response.recentActivities.map(
            (activity, index) => {
              // Determine activity type and icon based on status change
              let activityType = "modified";
              let activityIcon = "bi-pencil";
              let activityText = "";
              let iconBgClass = "bg-warning";

              if (activity.statusChanged === "completed") {
                activityType = "completed";
                activityIcon = "bi-check2";
                iconBgClass = "bg-success";
                activityText = `Completed "${activity.title}"`;
              } else if (activity.statusChanged === "in-progress") {
                activityType = "updated";
                activityIcon = "bi-pencil";
                iconBgClass = "bg-primary";
                activityText = `Updated "${activity.title}" to in-progress`;
              } else if (activity.statusChanged === "pending") {
                activityType = "created";
                activityIcon = "bi-plus-circle";
                iconBgClass = "bg-primary";
                activityText = `Created new task "${activity.title}"`;
              } else {
                activityText = `Modified "${activity.title}"`;
              }

              // Add category information if changed
              if (activity.categoryChanged) {
                activityText += ` in ${activity.categoryChanged}`;
              }

              return {
                id: index + 1,
                type: activityType,
                icon: activityIcon,
                iconBgClass: iconBgClass,
                text: activityText,
                time: this.formatRelativeTime(activity.updatedAt), // Since API doesn't provide timestamp, we'll use index-based time
                title: activity.title,
                status: activity.statusChanged,
                category: activity.categoryChanged,
                user: activity.userChanged || "user",
              };
            }
          );

          console.log("Transformed recent activities:", this.recentActivities);
        } else {
          console.warn("No recent activities found in response");
          this.recentActivities = [];
        }
      } catch (error) {
        console.error("Error fetching recent activity:", error);
        // Fallback to empty array if API fails
        this.recentActivities = [];
      }
    },
    formatRelativeTime(updatedAt) {
      const now = new Date();
      const updateTime = new Date(updatedAt);
      const diffInMinutes = Math.floor((now - updateTime) / (1000 * 60));

      if (diffInMinutes < 1) return "Just now";
      if (diffInMinutes < 60)
        return `${diffInMinutes} minute${diffInMinutes > 1 ? "s" : ""} ago`;

      const diffInHours = Math.floor(diffInMinutes / 60);
      if (diffInHours < 24)
        return `${diffInHours} hour${diffInHours > 1 ? "s" : ""} ago`;

      const diffInDays = Math.floor(diffInHours / 24);
      return `${diffInDays} day${diffInDays > 1 ? "s" : ""} ago`;
    },
    // Helper method to get category name by ID
    getCategoryNameById(categoryId) {
      const category = this.categories.find((cat) => cat.id == categoryId);
      return category ? category.name : "Uncategorized";
    },

    // Enhanced token handling
    getUserIdFromToken() {
      try {
        // Check for token in localStorage first with different possible names
        let token =
          localStorage.getItem("auth_token") ||
          localStorage.getItem("token") ||
          localStorage.getItem("jwt_token");

        // If not in localStorage, check cookies
        if (!token) {
          token =
            this.getCookieValue("auth_token") || this.getCookieValue("token");
        }

        if (!token) {
          console.error("No auth token found in localStorage or cookies");
          this.redirectToLogin();
          return null;
        }

        // Validate token format
        if (token.split(".").length !== 3) {
          console.error("Invalid JWT token format");
          this.clearAuthAndRedirect();
          return null;
        }

        // Decode JWT token to get userId
        const payload = JSON.parse(atob(token.split(".")[1]));
        console.log("Token payload:", payload);

        // Check if token is expired
        if (payload.exp && payload.exp < Date.now() / 1000) {
          console.error("Token has expired");
          this.clearAuthAndRedirect();
          return null;
        }

        // Try different possible userId fields
        const userId =
          payload.userId || payload.id || payload.sub || payload.user_id;

        if (!userId) {
          console.error("No userId found in token payload:", payload);
          return null;
        }

        console.log("Extracted userId from token:", userId);
        return userId;
      } catch (error) {
        console.error("Error decoding token:", error);
        this.clearAuthAndRedirect();
        return null;
      }
    },

    // Helper method to get cookie value
    getCookieValue(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(";").shift();
      return null;
    },

    // Clear authentication and redirect
    clearAuthAndRedirect() {
      localStorage.removeItem("auth_token");
      localStorage.removeItem("token");
      localStorage.removeItem("jwt_token");
      // Clear cookies if they exist
      document.cookie =
        "auth_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      document.cookie =
        "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      this.redirectToLogin();
    },

    // Redirect to login
    redirectToLogin() {
      // Replace with your actual login route
      console.log("Redirecting to login page...");
      // window.location.href = '/login';
      // Or if using Vue Router: this.$router.push('/login');
    },

    // Get authentication token for API requests
    getAuthToken() {
      return (
        localStorage.getItem("auth_token") ||
        localStorage.getItem("token") ||
        localStorage.getItem("jwt_token") ||
        this.getCookieValue("auth_token") ||
        this.getCookieValue("token")
      );
    },

    // Enhanced API method with authentication
    async makeAuthenticatedRequest(url, options = {}) {
      const token = this.getAuthToken();

      if (!token) {
        console.error("No token available for API request");
        this.redirectToLogin();
        return null;
      }

      const defaultOptions = {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        ...options,
      };

      // Merge headers properly
      if (options.headers) {
        defaultOptions.headers = {
          ...defaultOptions.headers,
          ...options.headers,
        };
      }

      try {
        console.log("Making API request to:", url);
        const response = await fetch(url, defaultOptions);

        if (response.status === 401) {
          console.error("Unauthorized request - token may be invalid");
          this.clearAuthAndRedirect();
          return null;
        }

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("API Response:", data);
        return data;
      } catch (error) {
        console.error("API request failed:", error);
        throw error;
      }
    },

    // Initialize user authentication
    initializeAuth() {
      const userId = this.getUserIdFromToken();
      if (userId) {
        this.userId = userId;
        console.log("User authenticated with ID:", this.userId);
        // Fetch initial data
        this.fetchAllData();
      } else {
        console.error("Failed to authenticate user");
        // You might want to show a login form or redirect here
      }
    },

    // NEW: Fetch all data including tasks and categories
    async fetchAllData() {
      if (!this.userId) {
        console.error("No userId available for data fetch");
        return;
      }

      this.loading = true;
      console.log("Fetching all data for userId:", this.userId);

      try {
        // Fetch categories first, then tasks (since tasks need categories for transformation)
        await this.fetchCategories();
        await this.fetchUserTasks();
        await this.fetchDashboardData();
        await this.fetchRecentActivity();
        console.log("All data loaded successfully");
      } catch (error) {
        console.error("Error fetching data:", error);
        alert("Failed to load data. Please refresh the page.");
      } finally {
        this.loading = false;
      }
    },

    // NEW: Fetch user tasks from API
    async fetchUserTasks() {
      try {
        console.log("Fetching tasks for user:", this.userId);
        const response = await this.makeAuthenticatedRequest(
          `http://localhost:3000/api/tasks/user/${this.userId}`
        );

        if (response) {
          console.log("Tasks API response:", response);

          // Handle different response structures
          let tasksData = response;
          if (response.data && Array.isArray(response.data)) {
            tasksData = response.data;
          } else if (response.tasks && Array.isArray(response.tasks)) {
            tasksData = response.tasks;
          } else if (!Array.isArray(response)) {
            console.warn("Unexpected tasks response structure:", response);
            tasksData = [];
          }

          // Transform API data to match component structure
          this.tasks = tasksData.map((task) => {
            // Get category name using categoryId and categories array
            const categoryId = task.category_id || task.categoryId;
            const categoryName = this.getCategoryNameById(categoryId);

            return {
              id: task.id,
              name: task.title || task.name || "Untitled Task",
              category: categoryName,
              dueDate:
                task.deadline ||
                task.dueDate ||
                new Date().toISOString().split("T")[0],
              status: task.status || "pending",
              completed: task.status === "completed" || task.completed || false,
              description: task.description || "",
              categoryId: categoryId || null,
            };
          });

          console.log("Transformed tasks:", this.tasks);

          // Update newTask userId
          this.newTask.userId = this.userId;
        }
      } catch (error) {
        console.error("Error fetching user tasks:", error);
        // Keep empty array if API fails
        this.tasks = [];
      }
    },

    // NEW: Fetch categories from API
    async fetchCategories() {
      try {
        console.log("Fetching categories");
        const response = await this.makeAuthenticatedRequest(
          "http://localhost:3000/api/category"
        );

        if (response) {
          console.log("Categories API response:", response);

          // Handle different response structures
          let categoriesData = response;
          if (response.data && Array.isArray(response.data)) {
            categoriesData = response.data;
          } else if (
            response.categories &&
            Array.isArray(response.categories)
          ) {
            categoriesData = response.categories;
          } else if (!Array.isArray(response)) {
            console.warn("Unexpected categories response structure:", response);
            categoriesData = [];
          }

          // Transform API data to match component structure
          this.categories = categoriesData.map((category) => ({
            id: category.id,
            name: category.name || "Unnamed Category",
          }));

          console.log("Transformed categories:", this.categories);
        }
      } catch (error) {
        console.error("Error fetching categories:", error);
        // Fallback to default categories if API fails
        this.categories = [
          { id: 1, name: "Design" },
          { id: 2, name: "Development" },
          { id: 3, name: "Marketing" },
          { id: 4, name: "QA" },
          { id: 5, name: "Documentation" },
        ];
      }
    },

    // API Methods with enhanced error handling
    async fetchDashboardData() {
      if (!this.userId) {
        console.error("No userId available for dashboard data fetch");
        return;
      }

      console.log("Fetching dashboard data for userId:", this.userId);

      try {
        await Promise.all([
          this.fetchTotalTasks(),
          this.fetchCompletedTasks(),
          this.fetchPriorityTasks(),
          this.fetchOverdueTasks(),
        ]);
        console.log("Dashboard data loaded successfully");
        console.log("Final apiData:", this.apiData);
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
        // Show user-friendly error message
        alert("Failed to load dashboard data. Please refresh the page.");
      }
    },

    async fetchTotalTasks() {
      try {
        const data = await this.makeAuthenticatedRequest(
          `http://localhost:3000/api/tasks/total?userId=${this.userId}`
        );
        if (data) {
          console.log("Total tasks response:", data);
          // Sesuaikan dengan response API yang sebenarnya
          this.apiData.totalTasks =
            data.totalCount ||
            data.total ||
            data.count ||
            data.totalTasks ||
            data.data?.total ||
            data.data?.count ||
            (Array.isArray(data) ? data.length : 0) ||
            (typeof data === "number" ? data : 0);
          console.log("Total tasks assigned:", this.apiData.totalTasks);
        }
      } catch (error) {
        console.error("Error fetching total tasks:", error);
      }
    },

    async fetchCompletedTasks() {
      try {
        const data = await this.makeAuthenticatedRequest(
          `http://localhost:3000/api/tasks/completed?userId=${this.userId}`
        );
        if (data) {
          console.log("Completed tasks response:", data);
          // Sesuaikan dengan response API yang sebenarnya
          this.apiData.completedTasks =
            data.completedCount ||
            data.completed ||
            data.count ||
            data.completedTasks ||
            data.data?.completed ||
            data.data?.count ||
            (Array.isArray(data) ? data.length : 0) ||
            (typeof data === "number" ? data : 0);
          console.log("Completed tasks assigned:", this.apiData.completedTasks);
        }
      } catch (error) {
        console.error("Error fetching completed tasks:", error);
      }
    },

    async fetchPriorityTasks() {
      try {
        const data = await this.makeAuthenticatedRequest(
          `http://localhost:3000/api/tasks/priority?userId=${this.userId}`
        );
        if (data) {
          console.log("Priority tasks response:", data);
          // Sesuaikan dengan response API yang sebenarnya
          this.apiData.upcomingTasks =
            data.priorityTasks ||
            data.upcoming ||
            data.priority ||
            data.count ||
            data.upcomingTasks ||
            data.data?.upcoming ||
            data.data?.priority ||
            data.data?.count ||
            (Array.isArray(data) ? data.length : 0) ||
            (typeof data === "number" ? data : 0);
          console.log(
            "Priority/Upcoming tasks assigned:",
            this.apiData.upcomingTasks
          );
        }
      } catch (error) {
        console.error("Error fetching priority tasks:", error);
      }
    },

    async fetchOverdueTasks() {
      try {
        const data = await this.makeAuthenticatedRequest(
          `http://localhost:3000/api/tasks/overdue?userId=${this.userId}`
        );
        if (data) {
          console.log("Overdue tasks response:", data);
          // Sesuaikan dengan response API yang sebenarnya
          this.apiData.overdueTasks =
            data.overdueCount ||
            data.overdue ||
            data.count ||
            data.overdueTasks ||
            data.data?.overdue ||
            data.data?.count ||
            (Array.isArray(data) ? data.length : 0) ||
            (typeof data === "number" ? data : 0);
          console.log("Overdue tasks assigned:", this.apiData.overdueTasks);
        }
      } catch (error) {
        console.error("Error fetching overdue tasks:", error);
      }
    },

    // Refresh all data
    async refreshAllData() {
      await this.fetchAllData();
    },

    // Refresh dashboard data
    async refreshDashboard() {
      await this.fetchDashboardData();
      await this.fetchRecentActivity();
    },

    changeView(view) {
      this.activeView = view;
      this.dropdownOpen = false;

      // Refresh data when switching to home view
      if (view === "home") {
        this.refreshDashboard();
      }
    },

    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },

    logout() {
      // Clear all possible token storage locations
      localStorage.removeItem("auth_token");
      localStorage.removeItem("token");
      localStorage.removeItem("jwt_token");

      // Clear cookies
      document.cookie =
        "auth_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      document.cookie =
        "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";

      alert("Logout successful!");
      this.dropdownOpen = false;

      // Reset user data
      this.userId = null;
      this.apiData = {
        totalTasks: 0,
        completedTasks: 0,
        upcomingTasks: 0,
        overdueTasks: 0,
      };
      this.tasks = [];
      this.categories = [];

      // Redirect to login page
      this.redirectToLogin();
    },

    editUser() {
      alert("Edit Profile!");
      this.dropdownOpen = false;
    },

    showSettings() {
      alert("Settings!");
      this.dropdownOpen = false;
    },

    formatDate(dateString) {
      const date = new Date(dateString);
      const userTimezoneOffset = date.getTimezoneOffset() * 60000;
      const correctedDate = new Date(date.getTime() + userTimezoneOffset);
      const options = { month: "short", day: "numeric", year: "numeric" };
      return correctedDate.toLocaleDateString("en-US", options);
    },

    getDateIn(days) {
      const date = new Date();
      date.setDate(date.getDate() + days);
      return date.toISOString().split("T")[0];
    },

    getCategoryClass(category, justColor = false) {
      const colors = {
        Design: { class: "category-design", color: "#ec4899" },
        Development: { class: "category-development", color: "#3b82f6" },
        Marketing: { class: "category-marketing", color: "#10b981" },
        QA: { class: "category-qa", color: "#f59e0b" },
        Documentation: { class: "category-documentation", color: "#8b5cf6" },
      };
      const style = colors[category] || {
        class: "category-default",
        color: "#64748b",
      };
      return justColor ? style.color : style.class;
    },

    getTaskCountByCategory(categoryName) {
      return this.tasks.filter((task) => task.category === categoryName).length;
    },

    toggleTaskDropdown() {
      this.showTaskDropdown = !this.showTaskDropdown;
    },

    selectTaskView(option) {
      this.selectedTaskView = option;
      this.showTaskDropdown = false;
    },

    openAddTaskForm() {
      this.showAddTaskForm = true;
      this.resetNewTask();
    },

    closeAddTaskForm() {
      this.showAddTaskForm = false;
    },

    resetNewTask() {
      this.newTask = {
        title: "",
        description: "",
        status: "pending",
        userId: this.userId || 1,
        categoryId: "",
        deadline: "",
      };
    },

    async addNewTask() {
      if (
        !this.newTask.title ||
        !this.newTask.categoryId ||
        !this.newTask.deadline
      ) {
        alert("Please fill in all required fields");
        return;
      }

      try {
        // Prepare task data for API
        const taskData = {
          title: this.newTask.title,
          description: this.newTask.description,
          status: this.newTask.status,
          userId: this.userId,
          categoryId: this.newTask.categoryId,
          deadline: this.newTask.deadline,
        };

        // Send to API
        const response = await this.makeAuthenticatedRequest(
          "http://localhost:3000/api/tasks",
          {
            method: "POST",
            body: JSON.stringify(taskData),
          }
        );

        if (response) {
          // Refresh tasks from API instead of manually adding
          await this.fetchUserTasks();
          await this.fetchRecentActivity();
          this.closeAddTaskForm();

          // Refresh dashboard data
          this.refreshDashboard();

          alert("Task added successfully!");
        }
      } catch (error) {
        console.error("Error adding new task:", error);
        alert("Failed to add task. Please try again.");
      }
    },

    toggleStatusDropdown(taskId) {
      const currentState = this.taskStatusDropdowns[taskId];
      this.closeAllCellDropdowns();
      this.taskStatusDropdowns[taskId] = !currentState;
    },

    toggleCategoryDropdown(taskId) {
      const currentState = this.taskCategoryDropdowns[taskId];
      this.closeAllCellDropdowns();
      this.taskCategoryDropdowns[taskId] = !currentState;
    },

    async updateTaskStatus(taskId, newStatus) {
      try {
        // Update via API
        const response = await this.makeAuthenticatedRequest(
          `http://localhost:3000/api/tasks/${taskId}/status`,
          {
            method: "PUT",
            body: JSON.stringify({ status: newStatus }),
          }
        );

        if (response) {
          // Refresh tasks from API instead of manually updating
          await this.fetchUserTasks();
          await this.fetchRecentActivity();

          // Refresh dashboard data
          this.refreshDashboard();
        }
      } catch (error) {
        console.error("Error updating task status:", error);
        alert("Failed to update task status. Please try again.");
      }

      this.taskStatusDropdowns[taskId] = false;
    },

    async updateTaskCategory(taskId, categoryId) {
      try {
        console.log(`Updating task ${taskId} to category ${categoryId}`);

        // Update via API
        const response = await this.makeAuthenticatedRequest(
          `http://localhost:3000/api/tasks/${taskId}/category`,
          {
            method: "PUT",
            body: JSON.stringify({ categoryId: categoryId }),
          }
        );

        if (response) {
          console.log("Category update response:", response);

          // Refresh tasks from API to get the updated data
          await this.fetchUserTasks();
          await this.fetchRecentActivity();

          console.log("Tasks refreshed after category update");
        }
      } catch (error) {
        console.error("Error updating task category:", error);
        alert("Failed to update task category. Please try again.");
      }

      this.taskCategoryDropdowns[taskId] = false;
    },

    getStatusClass(status) {
      const classes = {
        pending: "status-pending",
        completed: "status-completed",
        "in-progress": "status-progress",
      };
      return classes[status] || "status-pending";
    },

    closeAllCellDropdowns() {
      this.taskStatusDropdowns = {};
      this.taskCategoryDropdowns = {};
    },

    closeDropdownOnClickOutside(e) {
      if (
        this.dropdownOpen &&
        this.$el?.querySelector(".user-menu") &&
        !this.$el.querySelector(".user-menu").contains(e.target)
      ) {
        this.dropdownOpen = false;
      }
      if (
        this.showTaskDropdown &&
        this.$el?.querySelector(".task-filter-dropdown") &&
        !this.$el.querySelector(".task-filter-dropdown").contains(e.target)
      ) {
        this.showTaskDropdown = false;
      }
    },
  },

  mounted() {
    console.log("Dashboard component mounted");

    // Initialize authentication
    this.initializeAuth();

    // Add click outside listeners
    document.addEventListener("click", this.closeDropdownOnClickOutside);
  },

  beforeUnmount() {
    document.removeEventListener("click", this.closeDropdownOnClickOutside);
  },
};
</script>

<style scoped>
/* Desain CSS Anda yang sudah bagus ada di sini dan tidak akan saya ubah */
/* Cukup salin dan tempel seluruh blok style dari kode Anda sebelumnya ke sini */

* {
  box-sizing: border-box;
}

.dashboard-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
}

.sidebar {
  width: 280px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.1);
}

.sidebar-header {
  padding: 2rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-icon {
  font-size: 2.5rem;
  background: linear-gradient(45deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo-text {
  font-size: 1.75rem;
  font-weight: 700;
  background: linear-gradient(45deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-section {
  flex: 1;
  padding: 1rem;
}

.nav-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-links li {
  margin-bottom: 0.5rem;
  cursor: pointer;
}

.nav-links li a {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  color: #64748b;
  text-decoration: none;
  border-radius: 12px;
  transition: all 0.3s ease;
  font-weight: 500;
  position: relative;
  overflow: hidden;
}

.nav-links li a::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, #667eea, #764ba2);
  transition: left 0.3s ease;
  z-index: -1;
}

.nav-links li.active a,
.nav-links li a:hover {
  color: white;
  transform: translateX(8px);
}

.nav-links li.active a::before,
.nav-links li a:hover::before {
  left: 0;
}

.nav-links li a i {
  font-size: 1.25rem;
  width: 20px;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  margin: 1rem;
  margin-left: 0;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.main-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.header-title h2 {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  background: linear-gradient(45deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-subtitle {
  color: #64748b;
  margin: 0;
  font-size: 0.95rem;
}

.user-menu {
  position: relative;
}

.user-menu-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.user-menu-btn:hover {
  background: rgba(255, 255, 255, 1);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid rgba(102, 126, 234, 0.3);
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.user-name {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.9rem;
}

.user-role {
  font-size: 0.75rem;
  color: #64748b;
}

.dropdown-icon {
  transition: transform 0.3s ease;
  color: #64748b;
}

.dropdown-icon.rotated {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  padding: 0.5rem;
  min-width: 200px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  z-index: 1000;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: #334155;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.dropdown-item:hover {
  background: #f8fafc;
  color: #667eea;
}

.logout-item:hover {
  background: #fef2f2;
  color: #dc2626;
}

.dropdown-divider {
  height: 1px;
  background: rgba(0, 0, 0, 0.1);
  margin: 0.5rem 0;
}

.content-body {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.bg-gradient-primary {
  background: linear-gradient(45deg, #667eea, #764ba2);
}

.bg-gradient-success {
  background: linear-gradient(45deg, #11998e, #38ef7d);
}

.bg-gradient-warning {
  background: linear-gradient(45deg, #f093fb, #f5576c);
}

.bg-gradient-danger {
  background: linear-gradient(45deg, #f5365c, #f56036);
}

.stat-info {
  flex: 1;
}

.stat-label {
  color: #64748b;
  margin: 0;
  font-size: 0.85rem;
}

.stat-number {
  font-size: 1.75rem;
  font-weight: 600;
  margin: 0.25rem 0 0;
  color: #1e293b;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

.deadlines-card,
.activity-card,
.table-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.card-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.card-title h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: #1e293b;
}

.card-title p {
  color: #64748b;
  margin: 0.25rem 0 0 0;
  font-size: 0.9rem;
}

.card-body {
  padding: 1rem;
}

.deadline-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.deadline-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
  transition: all 0.2s ease;
}

.deadline-item:hover {
  background: #f1f5f9;
  transform: translateX(4px);
}

.deadline-info h4 {
  font-size: 0.95rem;
  font-weight: 600;
  margin: 0 0 0.25rem 0;
  color: #1e293b;
}

.deadline-info p {
  font-size: 0.8rem;
  color: #64748b;
  margin: 0;
}

.date-badge {
  background: #eef2ff;
  color: #4338ca;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.activity-text {
  color: #334155;
  margin: 0 0 0.25rem 0;
  font-size: 0.9rem;
  font-weight: 500;
}

.activity-time {
  color: #94a3b8;
  font-size: 0.8rem;
}

.bg-success {
  background: linear-gradient(45deg, #10b981, #34d399);
}

.bg-primary {
  background: linear-gradient(45deg, #3b82f6, #60a5fa);
}

.bg-warning {
  background: linear-gradient(45deg, #f59e0b, #fbbf24);
}

.view-table {
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.search-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-box i {
  position: absolute;
  left: 1rem;
  color: #94a3b8;
}

.search-box input {
  padding: 0.75rem 1rem 0.75rem 2.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  transition: all 0.3s ease;
  min-width: 250px;
}

.search-box input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.table-container {
  overflow-x: auto;
}

.modern-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.modern-table th,
.modern-table td {
  padding: 1rem 1.5rem;
  text-align: left;
  border-bottom: 1px solid #f1f5f9;
  white-space: nowrap;
}

.modern-table thead {
  background-color: #f8fafc;
}

.modern-table th {
  font-size: 0.8rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.modern-table tbody tr {
  transition: background-color 0.2s ease;
}

.modern-table tbody tr:hover {
  background-color: #f8fafc;
}

.id-badge {
  font-weight: 500;
  color: #64748b;
}

.category-badge,
.status-badge {
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: capitalize;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}
.category-design {
  background-color: #fce7f3;
  color: #db2777;
}
.category-development {
  background-color: #dbeafe;
  color: #2563eb;
}
.category-marketing {
  background-color: #d1fae5;
  color: #059669;
}
.category-qa {
  background-color: #fef3c7;
  color: #d97706;
}
.category-documentation {
  background-color: #e5e7eb;
  color: #4b5563;
}
.category-default {
  background-color: #f3f4f6;
  color: #374151;
}

.status-pending {
  background-color: #fef3c7;
  color: #d97706;
}
.status-completed {
  background-color: #d1fae5;
  color: #059669;
}
.status-progress {
  background-color: #dbeafe;
  color: #2563eb;
}

.color-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
}

.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  color: #94a3b8;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.empty-state p {
  font-size: 1.1rem;
  margin: 0;
  font-weight: 500;
}

.empty-row td {
  padding: 0;
}
.empty-row:hover {
  background: transparent !important;
}

.task-filter-dropdown {
  position: relative;
}

.filter-btn,
.add-task-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-btn {
  background-color: #fff;
  border: 1px solid #e2e8f0;
  color: #334155;
}

.filter-btn:hover {
  background-color: #f8fafc;
}

.add-task-btn {
  background-color: #5e72e4;
  color: white;
}
.add-task-btn:hover {
  background-color: #4f63d4;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(94, 114, 228, 0.2);
}

.filter-dropdown-menu {
  position: absolute;
  top: calc(100% + 5px);
  left: 0;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.07);
  z-index: 10;
  min-width: 180px;
  padding: 0.5rem;
}

.filter-dropdown-item {
  display: block;
  width: 100%;
  padding: 0.6rem 1rem;
  text-decoration: none;
  color: #334155;
  font-size: 0.9rem;
  border-radius: 6px;
  text-align: left;
}

.filter-dropdown-item:hover {
  background-color: #f8fafc;
}

.filter-dropdown-item.active {
  background-color: #eef2ff;
  color: #4338ca;
  font-weight: 600;
}

.dropdown-cell {
  position: relative;
}

.cell-dropdown-btn {
  border: 1px solid transparent;
  background-color: transparent;
}

.cell-dropdown-btn:hover {
  border-color: #e2e8f0;
}

.cell-dropdown-menu {
  position: absolute;
  top: calc(100% + 5px);
  right: 0;
  background: white;
  border-radius: 8px;
  padding: 0.5rem;
  min-width: 160px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  border: 1px solid #e2e8f0;
}

.cell-dropdown-item {
  display: block;
  padding: 0.5rem;
  border-radius: 6px;
}

.cell-dropdown-item:hover {
  background-color: #f8fafc;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(15, 23, 42, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  backdrop-filter: blur(8px);
  animation: overlay-in 0.3s ease-out;
}

@keyframes overlay-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-container {
  background: linear-gradient(135deg, #ffffff 0%, #7ab7f3 80%);
  border: 1px solid rgba(59, 130, 246, 0.1);
  border-radius: 20px;
  width: 90%;
  max-width: 520px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(59, 130, 246, 0.05);
  animation: modal-in 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  overflow: hidden;
}

@keyframes modal-in {
  from {
    opacity: 0;
    transform: translateY(-40px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 2rem 1rem 2rem;
  background: linear-gradient(135deg, var(--primary-color) 0%, #1d4ed8 100%);
  color: gray;
  position: relative;
}

.modal-header h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  position: relative;
  z-index: 1;
}

.modal-close-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.modal-close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.modal-body {
  padding: 2rem;
  max-height: 60vh;
  overflow-y: auto;
  background: var(--card-bg);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.75rem;
  font-weight: 600;
  color: var(--text-dark);
  font-size: 0.95rem;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 1rem 1.25rem;
  border: 2px solid var(--border-color);
  border-radius: 12px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  box-sizing: border-box;
}

.form-group input:hover,
.form-group select:hover,
.form-group textarea:hover {
  border-color: var(--primary-color);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  background: white;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1),
    0 8px 25px rgba(59, 130, 246, 0.15);
  transform: translateY(-2px);
}

.form-group select {
  cursor: pointer;
  appearance: none;
  background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="%233b82f6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>');
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 16px;
  padding-right: 3rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem 2rem 2rem 2rem;
  background: linear-gradient(135deg, #f8fafc 0%, #6e89a4 80%);
  border-top: 1px solid rgba(59, 130, 246, 0.1);
}

.btn {
  padding: 0.875rem 1.75rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border: none;
}

.btn-secondary {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  color: var(--text-dark);
  border: 2px solid var(--border-color);
}

.btn-secondary:hover {
  background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary-color) 0%, #1d4ed8 100%);
  color: white;
  border: 2px solid var(--primary-color);
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
}

.btn-primary:hover {
  background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
  transform: translateY(-3px);
  box-shadow: 0 12px 30px rgba(59, 130, 246, 0.4);
}
</style>
