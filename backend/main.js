const express = require("express");
const app = express();
const bodyParser = require("body-parser");
const userRoutes = require("./Routes/UserRoutes");
const taskRoutes = require("./Routes/TaskRoutes");
const categoryRoutes = require("./Routes/CategoryRoutes");
const sequelize = require("./config/database");
const setUpAssociations = require("./Models/associations");
const cors = require("cors");

const corsOptions = {
  origin: "http://localhost:5173",
};
app.use(cors(corsOptions));
app.use(bodyParser.json());
app.use("/api/users", userRoutes);
app.use("/api/tasks", taskRoutes);
app.use("/api/category", categoryRoutes);

setUpAssociations();

sequelize
  .sync()
  .then(() => {
    console.log("Database synced successfully");
    const port = process.env.PORT || 3000;
    app.listen(port, () => {
      console.log(`Server is running on port ${port}`);
    });
  })
  .catch((error) => {
    console.error("Error syncing database:", error);
  });
