import { BookingCreatePayload } from '@/types/booking';
import axios from 'axios';

export const getBookingsSummaries = async () => {
  const result = await axios.get(
    `${process.env.NEXT_PUBLIC_API_URL}/bookings/summaries`
  );
  return result.data;
};

export const postBooking = async (data: BookingCreatePayload) => {
  const result = await axios.post(
    `${process.env.NEXT_PUBLIC_API_URL}/bookings`,
    data
  );
  return result.data;
};
