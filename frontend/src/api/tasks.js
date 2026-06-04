import client from './client';

export const submitTasks = async (tasks) => {
  // tasks is { task1_done: bool, task2_done: bool, task3_done: bool }
  const response = await client.post('/tasks/submit', {
    task1_done: tasks.task1,
    task2_done: tasks.task2,
    task3_done: tasks.task3,
  });
  return response.data;
};

export const getTodayStatus = async () => {
  const response = await client.get('/tasks/today');
  return response.data;
};

export const getHistory = async (sprintId = null) => {
  const params = sprintId ? { sprint_id: sprintId } : {};
  const response = await client.get('/tasks/history', { params });
  return response.data;
};
