import { Model } from 'lux-framework';

class Task extends Model {
  static validates = {
    name: value => value.trim().length > 0,
  }
}

export default Task;
