import { Serializer } from 'lux-framework';

class TasksSerializer extends Serializer {
  attributes = [
    'isCompleted',
    'name',
  ];
}

export default TasksSerializer;
