const { Op } = require("sequelize");
const Task = require("../Models/Task");
const Category = require("../Models/Category");
const User = require("../Models/User");
const moment = require("moment-timezone");

const getAllTasks = async () => {
  try {
    return await Task.findAll({
      include: ["category"],
    });
  } catch (err) {
    throw new Error("Error fetching tasks");
  }
};
const getAllTasksByUserId = async (userId) => {
  try {
    const tasks = await Task.findAll({
      where: {
        user_id: userId, // Filter berdasarkan user_id
      },
      include: ["category"], // Sertakan data category untuk setiap task
    });
    return tasks;
  } catch (err) {
    console.error("Error fetching tasks for user:", err);
    throw new Error("Error fetching tasks for user");
  }
};
const createTask = async (
  title,
  description,
  status,
  userId,
  categoryId,
  deadline
) => {
  try {
    if (!userId || !categoryId) {
      throw new Error("Invalid user or category");
    }

    return await Task.create({
      title,
      description,
      status,
      user_id: userId,
      category_id: categoryId,
      deadline,
    });
  } catch (err) {
    console.error("Error creating Task:", err);
    throw new Error("Error creating task");
  }
};

const updateTask = async (
  id,
  title,
  description,
  status,
  userId,
  categoryId,
  deadline
) => {
  try {
    const task = await Task.findByPk(id);
    if (!task) {
      throw new Error("Task not found");
    }
    task.title = title;
    task.description = description;
    task.status = status;
    task.userId = userId;
    task.categoryId = categoryId;
    task.deadline = deadline;
    await task.save();
    return task;
  } catch (err) {
    console.error("Error creating Task:", err);
    throw new Error("Error updating task");
  }
};

const deleteTask = async (id) => {
  try {
    const task = await Task.findByPk(id);
    if (!task) {
      throw new Error("Task not found");
    }
    await task.destroy();
    return { message: "Task deleted successfully" };
  } catch (err) {
    throw new Error("Error deleting task");
  }
};
const getPriorityTasks = async (userId) => {
  const today = new Date();
  const upcomingDeadline = new Date(today);
  upcomingDeadline.setDate(today.getDate() + 3);

  const tasks = await Task.count({
    where: {
      user_id: userId,
      deadline: {
        [Op.lte]: upcomingDeadline,
      },
      status: {
        [Op.not]: "completed",
      },
    },
  });

  return tasks;
};
const getOverdueTasksCount = async (userId) => {
  const today = new Date();

  try {
    const overdueTasksCount = await Task.count({
      where: {
        user_id: userId,
        deadline: {
          [Op.lt]: today,
        },
        status: {
          [Op.not]: "completed",
        },
      },
    });

    return overdueTasksCount;
  } catch (err) {
    console.error("Error fetching overdue tasks count:", err);
    throw new Error("Error fetching overdue tasks count");
  }
};
// Count all tasks for a user
const getTotalTasksCount = async (userId) => {
  try {
    const totalTasksCount = await Task.count({
      where: {
        user_id: userId,
      },
    });
    return totalTasksCount;
  } catch (err) {
    console.error("Error fetching total tasks count:", err);
    throw new Error("Error fetching total tasks count");
  }
};

// Count completed tasks for a user
const getCompletedTasksCount = async (userId) => {
  try {
    const completedTasksCount = await Task.count({
      where: {
        user_id: userId,
        status: "completed", // Status task yang sudah selesai
      },
    });
    return completedTasksCount;
  } catch (err) {
    console.error("Error fetching completed tasks count:", err);
    throw new Error("Error fetching completed tasks count");
  }
};
const updateTaskStatus = async (id, status) => {
  try {
    const task = await Task.findByPk(id);
    if (!task) {
      throw new Error("Task not found");
    }
    task.status = status;
    await task.save();
    return task;
  } catch (err) {
    console.error("Error updating task status:", err);
    throw new Error("Error updating task status");
  }
};

const updateTaskCategory = async (id, categoryId) => {
  try {
    console.log(`Updating task ${id} with categoryId: ${categoryId}`);

    // Pastikan categoryId adalah number jika database mengharapkan number
    const parsedCategoryId = parseInt(categoryId);

    const task = await Task.findByPk(id);
    if (!task) {
      throw new Error("Task not found");
    }

    console.log(`Task found:`, task.toJSON());
    console.log(
      `Current categoryId: ${task.category_id}, New categoryId: ${parsedCategoryId}`
    );

    // Coba beberapa kemungkinan field name
    // Gunakan field name yang sesuai dengan model definition Anda
    task.category_id = parsedCategoryId; // atau task.categoryId = parsedCategoryId;

    // Force update dengan explicitly set changed
    task.changed("category_id", true); // atau task.changed('categoryId', true);

    const savedTask = await task.save();
    console.log(`Task updated:`, savedTask.toJSON());

    // Reload task dari database untuk memastikan data terbaru
    const refreshedTask = await Task.findByPk(id);
    console.log(`Refreshed task:`, refreshedTask.toJSON());

    return refreshedTask;
  } catch (err) {
    console.error("Error updating task category:", err);
    throw new Error("Error updating task category: " + err.message);
  }
};
async function getRecentActivity(userId) {
  try {
    const activities = await Task.findAll({
      where: { user_id: userId },
      order: [["updatedAt", "DESC"]],
      limit: 5,
      include: [
        {
          model: Category,
          as: "category",
          attributes: ["name"],
        },
        {
          model: User,
          as: "user",
          attributes: ["username"],
        },
      ],
    });

    const recentActivities = activities.map((task) => {
      const activity = {
        title: task.title,
        updatedAt: moment(task.updatedAt)
          .tz("Asia/Shanghai")
          .format("YYYY-MM-DD HH:mm:ss"), // Mengonversi ke zona waktu Beijing
      };

      if (task.status) {
        activity.statusChanged = task.status;
      }

      if (task.category && task.category.name) {
        activity.categoryChanged = task.category.name;
      }

      if (task.user && task.user.username) {
        activity.userChanged = task.user.username;
      }

      return activity;
    });

    return recentActivities;
  } catch (err) {
    console.error("Error get recent activity:", err);
    throw new Error(err.message);
  }
}

module.exports = {
  getAllTasks,
  createTask,
  updateTask,
  deleteTask,
  getPriorityTasks,
  getOverdueTasksCount,
  getTotalTasksCount, // Tambahkan ke ekspor
  getCompletedTasksCount,
  getAllTasksByUserId,
  updateTaskStatus,
  updateTaskCategory,
  getRecentActivity,
};
