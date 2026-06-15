import client from './client';

export const getSprints = async () => {
  const response = await client.get('/sprints');
  return response.data;
};

export const getCurrentSprint = async () => {
  const response = await client.get('/sprints/current');
  return response.data;
};

export const getCurrentSprintLeaderboard = async () => {
  const response = await client.get('/sprints/current/leaderboard');
  return response.data;
};

export const getSprintLeaderboard = async (sprintId) => {
  const response = await client.get(`/sprints/leaderboard/sprint/${sprintId}`);
  return response.data;
};
