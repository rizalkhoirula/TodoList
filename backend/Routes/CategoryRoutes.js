const express = require('express');
const categoryService = require('../Services/CategoryService');
const router = express.Router();

// Get all categories
router.get('/', async (req, res) => {
  try {
    const categories = await categoryService.getAllCategories();
    res.status(200).json(categories);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Create a new category
router.post('/', async (req, res) => {
  const { name } = req.body;
  try {
    const newCategory = await categoryService.createCategory(name);
    res.status(201).json({ message: 'Category created successfully', category: newCategory });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Update an existing category
router.put('/:id', async (req, res) => {
  const { id } = req.params;
  const { name } = req.body;
  try {
    const updatedCategory = await categoryService.updateCategory(id, name);
    res.status(200).json({ message: 'Category updated successfully', category: updatedCategory });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Delete a category
router.delete('/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const result = await categoryService.deleteCategory(id);
    res.status(200).json(result);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

module.exports = router;
