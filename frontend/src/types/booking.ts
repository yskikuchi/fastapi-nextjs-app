import { Car } from '@/types/Car';

type User = {
  name: string;
  email: string;
};

export type Booking = {
  id: string;
  user: User;
  car: Car;
  startTime: string;
  endTime: string;
  amount: number;
  status: string;
  referenceNumber: string;
  createdAt: string;
  updatedAt: string;
};

export type BookingCreatePayload = {
  carId: string;
  startTime: string;
  endTime: string;
  amount: number;
  user: {
    name: string;
    email: string;
  };
};
