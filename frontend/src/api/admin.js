import client from './client';

export const getUsers = async () => {
  const response = await client.get('/admin/users');
  return response.data;
};

export const getUserProgress = async (userId) => {
  const response = await client.get(`/admin/users/${userId}`);
  return response.data;
};

export const getUserHistory = async (userId) => {
  const response = await client.get(`/admin/users/${userId}/history`);
  return response.data;
};

export const getUserChart = async (userId) => {
  const response = await client.get(`/admin/users/${userId}/chart`);
  return response.data;
};

export const getLeaderboard = async () => {
  const response = await client.get('/admin/leaderboard');
  return response.data;
};

export const getLiveSessions = async () => {
  const response = await client.get('/admin/live-sessions');
  return response.data;
};

export const getLiveAttendanceForSession = async (sessionId) => {
  const response = await client.get(`/admin/live-attendance/${sessionId}`);
  return response.data;
};

export const validateLiveAttendance = async (sessionId, userId) => {
  const response = await client.post(`/admin/live-sessions/${sessionId}/validate/${userId}`);
  return response.data;
};
