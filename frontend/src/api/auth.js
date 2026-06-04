import client from './client';

export const login = async (email, password) => {
  const response = await client.post('/auth/login', { email, password });
  return response.data;
};

export const logout = async () => {
  const response = await client.post('/auth/logout');
  return response.data;
};

export const register = async (fullName, email, password, role = 'user') => {
  const response = await client.post('/auth/register', {
    full_name: fullName,
    email,
    password,
    role,
  });
  return response.data;
};
