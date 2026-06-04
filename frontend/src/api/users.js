import client from './client';

export const getMe = async () => {
  const response = await client.get('/users/me');
  return response.data;
};

export const getMyStats = async () => {
  const response = await client.get('/users/me/stats');
  return response.data;
};
