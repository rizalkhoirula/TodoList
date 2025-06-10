const User = require("./User"); 
const Task = require("./Task");
const Category = require("./Category");


const setUpAssociations = () => {

Task.belongsTo(User, {foreignKey: "user_id", as: "user", });
Task.belongsTo(Category, {foreignKey: "category_id",as: "category",});
Category.hasMany(Task, { foreignKey: "category_id", as: "tasks" });


};

module.exports = setUpAssociations;
