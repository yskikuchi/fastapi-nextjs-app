import axios from 'axios';

export const getCars = async () => {
  const result = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/cars`);
  return result.data;
};
