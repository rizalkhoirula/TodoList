const express = require("express");
const taskService = require("../Services/TaskService");
const router = express.Router();

// Get all tasks
router.get("/", async (req, res) => {
  try {
    const tasks = await taskService.getAllTasks();
    res.status(200).json(tasks);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Create a new task
router.post("/", async (req, res) => {
  const { title, description, status, userId, categoryId, deadline } = req.body;
  try {
    const newTask = await taskService.createTask(
      title,
      description,
      status,
      userId,
      categoryId,
      deadline
    );
    res
      .status(201)
      .json({ message: "Task created successfully", task: newTask });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Update an existing task
router.put("/:id", async (req, res) => {
  const { id } = req.params;
  const { title, description, status, userId, categoryId, deadline } = req.body;
  try {
    const updatedTask = await taskService.updateTask(
      id,
      title,
      description,
      status,
      userId,
      categoryId,
      deadline
    );
    res
      .status(200)
      .json({ message: "Task updated successfully", task: updatedTask });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Delete a task
router.delete("/:id", async (req, res) => {
  const { id } = req.params;
  try {
    const result = await taskService.deleteTask(id);
    res.status(200).json(result);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});
router.get("/overdue", async (req, res) => {
  const { userId } = req.query; // Assuming userId is passed as a query parameter
  if (!userId) {
    return res.status(400).json({ message: "User ID is required" });
  }

  try {
    const overdueCount = await taskService.getOverdueTasksCount(userId);
    res.status(200).json({ overdueCount });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});
// Get total count of tasks for a user
router.get("/total", async (req, res) => {
  const { userId } = req.query;
  if (!userId) {
    return res.status(400).json({ message: "User ID is required" });
  }

  try {
    const totalCount = await taskService.getTotalTasksCount(userId);
    res.status(200).json({ totalCount });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Get count of completed tasks for a user
router.get("/completed", async (req, res) => {
  const { userId } = req.query;
  if (!userId) {
    return res.status(400).json({ message: "User ID is required" });
  }

  try {
    const completedCount = await taskService.getCompletedTasksCount(userId);
    res.status(200).json({ completedCount });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});
router.get("/priority", async (req, res) => {
  const { userId } = req.query; // Assuming userId is passed as a query parameter
  if (!userId) {
    return res.status(400).json({ message: "User ID is required" });
  }

  try {
    const priorityTasks = await taskService.getPriorityTasks(userId);
    res.status(200).json({ priorityTasks });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});
router.get("/user/:userId", async (req, res) => {
  const { userId } = req.params; // Mengambil userId dari parameter URL

  try {
    const tasks = await taskService.getAllTasksByUserId(userId); // Panggil fungsi untuk mendapatkan task berdasarkan userId
    res.status(200).json(tasks);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});
router.put("/:id/status", async (req, res) => {
  const { id } = req.params;
  const { status } = req.body; // New status

  try {
    const updatedTask = await taskService.updateTaskStatus(id, status);
    res
      .status(200)
      .json({ message: "Task status updated successfully", task: updatedTask });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

/// Update task category - Fixed router
router.put("/:id/category", async (req, res) => {
  const { id } = req.params;
  const { categoryId } = req.body; // New category ID

  // Validation
  if (!categoryId) {
    return res.status(400).json({ message: "categoryId is required" });
  }

  console.log(`Router: Updating task ${id} to categoryId ${categoryId}`);

  try {
    const updatedTask = await taskService.updateTaskCategory(id, categoryId);

    console.log(`Router: Task updated successfully:`, updatedTask.toJSON());

    res.status(200).json({
      message: "Task category updated successfully",
      task: updatedTask,
    });
  } catch (err) {
    console.error(`Router: Error updating task category:`, err);
    res.status(500).json({ message: err.message });
  }
});
// Router: tasks.js
router.get("/recent-activity", async (req, res) => {
  const { userId } = req.query; // Ambil userId dari query parameter

  if (!userId) {
    return res.status(400).json({ message: "User ID is required" });
  }

  try {
    const recentActivities = await taskService.getRecentActivity(userId);
    res.status(200).json({ recentActivities });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

module.exports = router;
