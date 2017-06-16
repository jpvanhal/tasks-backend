export default {
  development: {
    driver: 'sqlite3',
    database: 'backend_dev'
  },

  test: {
    driver: 'sqlite3',
    database: 'backend_test'
  },

  production: {
    driver: 'sqlite3',
    database: 'backend_prod'
  }
};
