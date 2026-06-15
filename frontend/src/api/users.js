import client from './client';

export const getUsers = async () => {
  const response = await client.get('/users/');
  return response.data;
};


export const getMyStats = async () => {
  const response = await client.get('/users/me/stats');
  return response.data;
};
