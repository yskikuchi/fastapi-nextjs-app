import { Car } from './Car';

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
