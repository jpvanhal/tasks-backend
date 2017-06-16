export default {
  development: {
    driver: 'pg',
    database: 'tasks_dev'
  },

  test: {
    driver: 'pg',
    database: 'tasks_test'
  },

  production: {
    driver: 'pg',
    database: 'tasks_prod'
  }
};
