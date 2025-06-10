const { Op } = require("sequelize");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const User = require("../Models/User");
const Task = require("../Models/Task");
const Category = require("../Models/Category");

const registerUser = async (req, res) => {
  const { username, email, password } = req.body;

  try {
    const existingUser = await User.findOne({ where: { email } });
    if (existingUser) {
      return res.status(400).json({ message: "Email already in use" });
    }

    const newUser = await User.create({ username, email, password });
    res
      .status(201)
      .json({ message: "User created successfully", user: newUser });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error creating user", error });
  }
};

const loginUser = async (req, res) => {
  const { email, password } = req.body;

  try {
    const user = await User.findOne({ where: { email } });
    if (!user) {
      return res.status(404).json({ message: "User not found" });
    }

    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      return res.status(401).json({ message: "Invalid credentials" });
    }

    const token = jwt.sign(
      { id: user.id, username: user.username },
      process.env.JWT_SECRET,
      { expiresIn: "1d" }
    );

    // Cek tugas yang mendekati deadline (misalnya dalam 2 hari)
    const today = new Date();
    const twoDaysFromNow = new Date(today);
    twoDaysFromNow.setDate(today.getDate() + 2);

    const urgentTasks = await Task.findAll({
      where: {
        user_id: user.id,
        deadline: {
          [Op.lte]: twoDaysFromNow.setHours(0, 0, 0, 0), // Deadline <= 2 hari ke depan
        },
      },
      include: ["category"], // Include category jika perlu
    });

    // Menampilkan pesan jika ada tugas prioritas tinggi
    const taskPriorityMessage =
      urgentTasks.length > 0
        ? `You have ${urgentTasks.length} task(s) with priority deadline!`
        : "No priority tasks at the moment.";

    res.status(200).json({
      message: "Login successful",
      token,
      taskPriorityMessage, // Tampilkan pesan prioritas tugas
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error logging in", error });
  }
};


module.exports = {
  registerUser,
  loginUser,
};
