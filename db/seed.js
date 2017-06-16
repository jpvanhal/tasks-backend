import faker from 'faker';

import Task from '../app/models/task';
import range from '../app/utils/range';

const {
  hacker,
  random,
} = faker;

export default async function seed(trx) {
  await Promise.all(
    Array.from(range(1, 100)).map(() => (
      Task.transacting(trx).create({
        name: hacker.phrase(),
        isCompleted: random.boolean(),
      })
    ))
  );
}
