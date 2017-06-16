import { Controller } from 'lux-framework';

class TasksController extends Controller {
  params = [
    'isCompleted',
    'name',
  ];
}

export default TasksController;
