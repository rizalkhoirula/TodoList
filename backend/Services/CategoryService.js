const Category = require("../Models/Category");

const getAllCategories = async () => {
  try {
    return await Category.findAll();
  } catch (err) {
    throw new Error("Error fetching categories");
  }
};

const createCategory = async (name) => {
  try {
    return await Category.create({ name });
  } catch (err) {
    console.error("Error creating category:", err);
    throw new Error("Error creating category");
  }
};

const updateCategory = async (id, name) => {
  try {
    const category = await Category.findByPk(id);
    if (!category) {
      throw new Error("Category not found");
    }
    category.name = name;
    await category.save();
    return category;
  } catch (err) {
    console.error("Error updating category:", err);
    throw new Error("Error updating category");
  }
};

const deleteCategory = async (id) => {
  try {
    const category = await Category.findByPk(id);
    if (!category) {
      throw new Error("Category not found");
    }
    await category.destroy();
    return { message: "Category deleted successfully" };
  } catch (err) {
    throw new Error("Error deleting category");
  }
};

module.exports = {
  getAllCategories,
  createCategory,
  updateCategory,
  deleteCategory,
};
