require('dotenv').config(); 

const { Sequelize } = require('sequelize');

const sequelize = new Sequelize({
  dialect: process.env.DB_DIALECT,
  host: process.env.DB_HOST,  
  username: process.env.DB_USER,  
  password: process.env.DB_PASSWORD, 
  database: process.env.DB_NAME, 
  logging: false,
});

module.exports = sequelize;
